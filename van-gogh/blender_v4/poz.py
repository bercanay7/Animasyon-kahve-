# -*- coding: utf-8 -*-
"""Mixamo iskeletli (MPFB "mixamo" rig) figürleri dünya yönleriyle pozlama.

Uzuv yönü: kemiğin başından çocuk kemiğin başına. Dönüşler dünya ekseni etrafında, kemik başında.
Canlandırma: her karede temel poza dönülür, üstüne zamanın işlevi olan küçük dönüşler eklenir, anahtarlanır.
"""
import math
import bpy
from mathutils import Vector, Quaternion, Matrix

UP = Vector((0, 0, 1))
P = "mixamorig:"


def yumusak(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def gecis(t, t0, sure):
    """t0'da başlayan, `sure` saniyede 0→1 yumuşak geçiş."""
    return yumusak((t - t0) / max(sure, 1e-6))


class Figur:
    def __init__(self, iskelet):
        self.a = iskelet
        self.pb = iskelet.pose.bones
        for b in self.pb:
            b.rotation_mode = 'QUATERNION'
        self.cocuk = {}
        for yan in ("Left", "Right"):
            c = self.cocuk
            c[P + yan + "Arm"] = P + yan + "ForeArm"
            c[P + yan + "ForeArm"] = P + yan + "Hand"
            c[P + yan + "Hand"] = P + yan + "HandMiddle1"
            for f in ("Thumb", "Index", "Middle", "Ring", "Pinky"):
                c[P + yan + "Hand" + f + "1"] = P + yan + "Hand" + f + "2"
                c[P + yan + "Hand" + f + "2"] = P + yan + "Hand" + f + "3"
            c[P + yan + "UpLeg"] = P + yan + "Leg"
            c[P + yan + "Leg"] = P + yan + "Foot"
            c[P + yan + "Shoulder"] = P + yan + "Arm"
        self.cocuk[P + "Neck"] = P + "Head"
        self.cocuk[P + "Spine2"] = P + "Neck"
        self.guncelle()
        f = (self.bas(P + "LeftToeBase") + self.bas(P + "RightToeBase")) - (self.bas(P + "LeftFoot") + self.bas(P + "RightFoot"))
        f.z = 0
        self.on0 = f.normalized()                      # içe alındığındaki ön yön (dünya)
        self.temel = None

    # ------------------------------------------------ temel
    def guncelle(self):
        bpy.context.view_layer.update()

    def bas(self, ad):
        return self.a.matrix_world @ self.pb[ad].head

    def kuyruk(self, ad):
        return self.a.matrix_world @ self.pb[ad].tail

    def uzuv(self, ad):
        if ad in self.cocuk:
            return (self.bas(self.cocuk[ad]) - self.bas(ad)).normalized()
        for k, v in self.cocuk.items():
            if v == ad:
                return (self.bas(ad) - self.bas(k)).normalized()
        return (self.kuyruk(ad) - self.bas(ad)).normalized()

    @property
    def on(self):
        q = self.a.matrix_world.to_quaternion()
        v = q @ (self.a.matrix_world.to_quaternion().inverted() @ self.on0)
        f = (self.bas(P + "LeftToeBase") + self.bas(P + "RightToeBase")) - (self.bas(P + "LeftFoot") + self.bas(P + "RightFoot"))
        f.z = 0
        return f.normalized()

    @property
    def sag(self):  # karakterin kendi sağı; bu eksen etrafında + dönüş başı/gövdeyi geriye-yukarı alır
        return self.on.cross(UP).normalized()

    def dondur(self, ad, eksen, aci, guncelle=True):
        """Kemiği dünya ekseni etrafında kendi başında döndür."""
        if abs(aci) < 1e-7:
            return
        pb = self.pb[ad]
        qa = self.a.matrix_world.to_quaternion()
        e = (qa.inverted() @ Vector(eksen)).normalized()
        R = pb.matrix.to_quaternion()
        pb.rotation_quaternion = pb.rotation_quaternion @ (R.inverted() @ Quaternion(e, aci) @ R)
        if guncelle:
            self.guncelle()

    def yonelt(self, ad, hedef, oran=1.0):
        d = self.uzuv(ad)
        t = Vector(hedef).normalized()
        e = d.cross(t)
        if e.length < 1e-6:
            return
        self.dondur(ad, e.normalized(), d.angle(t) * oran)

    def dis(self, yan):
        v = self.bas(P + yan + "Arm") - self.bas(P + "Spine2")
        v.z = 0
        return v.normalized()

    def avuc(self, yan):
        h = self.bas(P + yan + "Hand")
        a = self.bas(P + yan + "HandIndex1"); b = self.bas(P + yan + "HandPinky1")
        d = ((a + b) / 2 - h).normalized()
        n = d.cross(a - b).normalized()
        if n.dot(-self.dis(yan)) < 0:
            n = -n
        return n, d

    def parmak(self, yan, acilar=(0.16, 0.28, 0.22), bas_p=(0.08, 0.12, 0.08)):
        n, _ = self.avuc(yan)
        for i, f in enumerate(("Index", "Middle", "Ring", "Pinky")):
            for seg, aci in zip("123", acilar):
                ad = P + yan + "Hand" + f + seg
                e = self.uzuv(ad).cross(n)
                if e.length > 1e-6:
                    self.dondur(ad, e.normalized(), aci * (1 + 0.12 * i))
        for seg, aci in zip("123", bas_p):
            ad = P + yan + "HandThumb" + seg
            e = self.uzuv(ad).cross(n)
            if e.length > 1e-6:
                self.dondur(ad, e.normalized(), aci)

    # ------------------------------------------------ hazır duruşlar
    def ayakta(self, sag_dirsek=0.25, sol_dirsek=0.25, kollar_on=0.06):
        """A pozdan doğal ayakta duruş: kollar aşağı, dirsekler hafif bükük, parmaklar gevşek."""
        for yan, dz in (("Left", sol_dirsek), ("Right", sag_dirsek)):
            o = self.dis(yan)
            self.yonelt(P + yan + "Arm", -UP + o * 0.16 + self.on * kollar_on)
            self.yonelt(P + yan + "ForeArm", -UP + self.on * dz + o * 0.04)
            self.yonelt(P + yan + "Hand", self.uzuv(P + yan + "ForeArm") - o * 0.12)
            self.parmak(yan)

    def kaydet(self):
        self.temel = {b.name: b.rotation_quaternion.copy() for b in self.pb}

    def sifirla(self):
        for b in self.pb:
            b.rotation_quaternion = self.temel[b.name].copy()
        self.guncelle()

    def nefes(self, t, faz=0.0, guc=1.0):
        n = math.sin(2 * math.pi * (t / 4.2 + faz))
        self.dondur(P + "Spine1", self.sag, math.radians(0.8) * n * guc)
        self.dondur(P + "Spine2", self.sag, math.radians(1.0) * n * guc)
        self.dondur(P + "LeftShoulder", self.on, math.radians(0.7) * n * guc)
        self.dondur(P + "RightShoulder", self.on, -math.radians(0.7) * n * guc)
        self.dondur(P + "Hips", self.on, math.radians(0.5) * math.sin(2 * math.pi * (t / 6.3 + faz)) * guc)

    def bak(self, hedef, oran=1.0, boyun=0.35):
        """Başı (ve boynu) dünya noktasına çevir (yatay + dikey)."""
        bas = self.bas(P + "Head") + UP * 0.08
        d = (Vector(hedef) - bas).normalized()
        on = self.on
        # yatay
        dy = Vector((d.x, d.y, 0)).normalized()
        yaw = math.atan2(on.cross(dy).z, on.dot(dy)) * oran
        self.dondur(P + "Neck", UP, yaw * boyun)
        self.dondur(P + "Head", UP, yaw * (1 - boyun))
        # dikey (pozitif: aşağı bakış)
        pitch = math.asin(max(-1, min(1, d.z))) * oran   # sağ eksen etrafında + = yukarı
        yan = self.on.cross(UP).normalized()
        self.dondur(P + "Neck", yan, pitch * boyun)
        self.dondur(P + "Head", yan, pitch * (1 - boyun))

    # ------------------------------------------------ yerleştirme
    def yerlestir(self, konum, bakis):
        """Ayakları yere, ön yönü `bakis` (dünya xy) noktasına/vektörüne."""
        hedef = Vector(bakis) - Vector((konum[0], konum[1], 0))   # bakis: dünya noktası
        hedef.z = 0
        hedef.normalize()
        on = self.on
        aci = math.atan2(on.cross(hedef).z, on.dot(hedef))
        self.a.rotation_mode = 'XYZ'
        self.a.rotation_euler.z += aci
        self.guncelle()
        self.a.location.x += konum[0] - self.a.location.x
        self.a.location.y += konum[1] - self.a.location.y
        self.guncelle()

    def bagla(self, nesne, kemik, dunya_matrisi):
        nesne.parent = self.a
        nesne.parent_type = 'BONE'
        nesne.parent_bone = kemik
        self.guncelle()
        nesne.matrix_world = dunya_matrisi
        self.guncelle()

    def anahtarla(self, kare):
        for b in self.pb:
            b.keyframe_insert("rotation_quaternion", frame=kare)

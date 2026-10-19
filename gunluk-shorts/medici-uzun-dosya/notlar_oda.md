# İç mekân dünyası — Lab-D notları (`cilt_oda.py`, `preview_oda.py`)

Durum (teslim sırası, her ön ayar bitince güncellenir):
| # | ön ayar | durum |
|---|---|---|
| 1 | `room="oda1743"` | HAZIR (gece/gün, `path="in"/"out"`, oturan/yatan siluet, belgeye zum) |
| 2 | `room="salon"` (`variant=medici/napoli/signoria/pitti`) | HAZIR |
| 3 | `room="banka"` | HAZIR (gündüz/gece, şube kapanışı `close_at`) |
| 4 | `room="calisma"` (hucre/kutuphane/studiolo) | yapılıyor |
| 5 | `room="sakristi"` | sırada |
| 6 | `room="bos"` (blois/koln) | sırada |
| 7 | `room="perde"` | sırada (düşük öncelik) |
| 8 | yeniden kullanılabilir işlevler | `candle, oil_lamp, window_light, table, door_bronze, quill, inkwell, doc_sheet, sil_actor, seated, chandelier, candelabra_table, balance_scale, map_sheet` hazır |

## 1. API (ayrıntılı sürüm teslimde)

```python
shot("oda", a, room="oda1743", path="in", figure="seated", mode="night", cam=None, link="scale", tr=("zoomthru", 1.0, dict(at=(1050, 540))))
shot("oda", a, room="salon", variant="napoli", mode="night", path="heads", cam=("rack", (330, 700), (1560, 700), dict(at=("c8s9","rehine",0), dur=1.6, r=380)))
shot("oda", a, room="banka", mode="night", path="close", close_at=("c9s7", 0), close_dur=8.0)
```
Ortak parametreler: `room, variant, tod|mode ("day"|"dusk"|"night"), path | cams=[(çapa,(x,y,zoom)),…], actors=[dict(kind,x,y,h,action,at,dir,seed,sil,seated,walk,prop,layer)], props=[…], kick, caption, at, frame (True|False|"auto"), seed`.
`actors` verilmezse odanın varsayılan figürleri; verilirse (boş liste dâhil) yalnız onlar çizilir.

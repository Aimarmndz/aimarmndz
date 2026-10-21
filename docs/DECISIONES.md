# Decisiones

## 2026-10-21 · Rediseño del perfil con estética de terminal

**Contexto.** El README del perfil acumulaba badges de colores distintos,
repetía portfolio y email tres veces y dependía de servicios externos que
fallaban: `github-profile-trophy.vercel.app` y
`github-readme-activity-graph.vercel.app` devolvían `402 DEPLOYMENT_DISABLED`
(imágenes rotas) y la tarjeta de `github-readme-stats` mostraba 0 commits y
rango C porque la instancia pública no cuenta repos privados.

**Decisión.**
- Banner propio en SVG versionado en `assets/` (`banner-dark.svg` y
  `banner-light.svg`), servido con `<picture>` según el tema del visitante.
  Sustituye a `readme-typing-svg.herokuapp.com`.
- Paleta de GitHub (`#0d1117`, `#21262d`, `#30363d`) con un único acento
  verde: `#3fb950` en oscuro y `#1a7f37` en claro, porque el primero no
  llega a 4.5:1 sobre blanco.
- Los SVG usan la fuente monoespaciada del sistema: GitHub los sirve como
  imagen y no cargan fuentes externas. El cursor parpadea con CSS y se
  detiene con `prefers-reduced-motion`.
- Badges uniformes en `#21262d` con logo blanco. Visitas y seguidores en
  `#238636`, que con texto blanco sí pasa contraste (komarev no admite
  color de etiqueta).
- Fuera las tarjetas de stats, top languages, trofeos y gráfica de
  actividad. Se mantiene la serpiente (workflow propio) y se añade la
  tarjeta de racha en `streak-stats.demolab.com`, el dominio actual del
  servicio.
- Nueva sección de proyectos con los repos públicos scan2nas, orgtable y
  vibe-gambling, con textos tomados de sus propias descripciones.
- La maqueta de referencia está en Claude Design:
  https://claude.ai/artifact/W19JKC1tkDJSH1pME5Bhwh

**Alternativas descartadas.**
- Tarjetas `api/pin` de github-readme-stats para los proyectos: misma
  instancia pública inestable; una tabla Markdown no depende de nadie.
- Títulos coloreados con LaTeX (`$\color{}$`): se ven mal y no son texto
  real. Los títulos `~/about`, `~/now`… quedan en el color normal.
- Desplegar una instancia propia de github-readme-stats: más mantenimiento
  del que justifica un perfil.

**Consecuencias.**
- Cambiar el texto del banner implica editar los dos SVG a la vez.
- La tarjeta de racha y los contadores siguen dependiendo de servicios
  externos; si caen, se quitan en vez de dejar imágenes rotas.
- Este repo es el README del perfil, así que no sigue la estructura fija de
  README de proyecto.

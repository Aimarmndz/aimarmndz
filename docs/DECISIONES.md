# Decisiones

## 2026-10-21 · Badges estáticos sin servicios externos

**Contexto.** Con el perfil ya publicado, los badges de shields.io y el
contador de komarev fallaban de forma intermitente: GitHub sirve las
imágenes externas a través de su proxy (camo) y algunas cargas se cortaban,
dejando iconos rotos (Discord en dos de tres recargas). El usuario pidió no
depender de servicios externos. Además, el perfil estaba marcado como
privado y la tarjeta de racha y la serpiente salían a cero; se ha vuelto a
poner público desde los ajustes de GitHub.

**Decisión.**
- Todos los badges (contacto, stack y Ko-fi) son SVG versionados en
  `assets/badges/`, con variante clara y oscura servidas con `<picture>`.
- Se generan con `scripts/build_badges.py` (solo librería estándar):
  cambiar un badge es editar sus listas y volver a ejecutarlo.
- Texto monoespaciado con `textLength`: el ancho se calcula sin métricas de
  fuente y se respeta aunque el visitante tenga otra monoespaciada.
- Iconos de trazo propios en vez de logos de marca: evitan depender de
  Simple Icons, que ya retiró LinkedIn y VS Code.
- Fuera el contador de visitas (komarev) y la tarjeta de racha
  (streak-stats): no se pueden servir en estático. Queda la serpiente, que
  genera el workflow propio y se sirve desde el propio GitHub.

**Alternativas descartadas.**
- Mantener shields.io con reintentos: el corte lo hace el proxy de GitHub,
  no se controla desde el README.
- Un SVG por chip del stack: 21 archivos por tema; una fila por categoría
  basta y se reduce sola en pantallas estrechas.

**Consecuencias.**
- Los SVG generados no se editan a mano: se cambia el script y se
  regenera.
- El perfil no muestra visitas ni racha; el gráfico de contribuciones de
  GitHub ya aparece justo debajo del README.

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
- Badges uniformes en `#21262d` con logo blanco. Visitas en `#238636`, que
  con texto blanco sí pasa contraste (komarev no admite color de etiqueta).
- Simple Icons ya no incluye los logos de LinkedIn ni de VS Code: esos dos
  badges llevan un icono de trazo propio incrustado en base64.
- Fuera el badge de seguidores: shields devuelve 0 (hay 10) y GitHub ya los
  muestra en la barra lateral.
- La tabla del stack va en HTML: en Markdown una tabla sin cabecera pinta
  una fila vacía.
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

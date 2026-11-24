import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const GardenIdentity: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const root = pathToRoot(fileData.slug!)
  return (
    <section class={`garden-identity ${displayClass ?? ""}`}>
      <a href={root} class="garden-portrait-link" aria-label="Inicio del jardín de Elver Chaparro">
        <img class="garden-portrait" src={`${root}/adjuntos/elver-chaparro-cardozo.jpg`} alt="Elver Chaparro Cardozo" width="144" height="144" />
      </a>
      <h2 class="page-title"><a href={root}>{cfg.pageTitle}</a></h2>
      <p class="garden-subtitle">Notas, imágenes y conexiones para pensar.</p>
      <nav aria-label="Navegación del jardín" class="garden-navigation">
        <a href={root}>Inicio</a>
        <a href={`${root}/ahora`}>Ahora</a>
        <a href={`${root}/acerca`}>Acerca del jardín</a>
        <a href={`${root}/licencia`}>Licencia</a>
        <a href="https://elverchaparrolab.wordpress.com/">Sitio principal</a>
      </nav>
    </section>
  )
}
export default (() => GardenIdentity) satisfies QuartzComponentConstructor

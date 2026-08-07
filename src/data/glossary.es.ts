/**
 * L2 glossary, Spanish. Transcribed verbatim from web/content/es/_common.md.
 *
 * Same fifteen terms as the English one, and the KEYS are not always the same
 * string: two of them are translated ("esquema CB", "compensación de junta
 * fría") because they are translated in the copy. The English file is not a
 * template to be filled in, it is a sibling.
 *
 * Same convention as English: a term is marked ONCE per page, on its first
 * occurrence.
 */
export const GLOSSARY: Record<string, string> = {
  'bare metal':
    'Código que corre directamente sobre el microcontrolador, sin sistema operativo debajo.',
  pinout:
    'La asignación de cada patilla física del microcontrolador a una función. Fijarlo decide qué van a poder hacer el hardware y el software.',
  HAL:
    'Capa de abstracción de hardware: la capa fina que permite que el mismo código de aplicación corra sobre otro microcontrolador.',
  'Class B':
    'La categoría de software relacionado con la seguridad que definen las normas del electrodoméstico. Prescribe qué tiene que detectar el software sobre sus propios fallos, y cómo hay que demostrarlo.',
  PEC:
    'Circuito electrónico de protección: hardware cuyo trabajo es llevar el aparato a un estado seguro cuando algo falla.',
  'esquema CB':
    'Acuerdo internacional por el que el informe de ensayo de un organismo de certificación lo aceptan los demás, en vez de volver a ensayar en cada país.',
  'VDE, UL':
    'Organismos de certificación, alemán y estadounidense respectivamente, que evalúan y certifican producto eléctrico.',
  PID:
    'La ley de control realimentado estándar: corrige con el error actual, con su historia acumulada y con su velocidad de cambio.',
  FOPDT:
    'Primer orden con retardo: un modelo matemático sencillo de cómo responde un sistema físico lento, que sirve para ajustar el lazo de control antes de tocar el aparato real.',
  'compensación de junta fría':
    'Un termopar mide una diferencia de temperatura, así que para obtener una lectura absoluta hace falta la temperatura del otro extremo del hilo, y hay que corregir por ella.',
  'V-Model':
    'Proceso de desarrollo que empareja cada paso de especificación con el ensayo que lo demuestra.',
  ALM:
    'Gestión del ciclo de vida de la aplicación: las herramientas que mantienen requisitos, tareas y ensayos en un mismo sitio trazable.',
  'fin de línea':
    'La última estación de ensayo de una línea de producción, donde se comprueba cada unidad antes de expedirla.',
  'DALI, DMX': 'Protocolos estándar de comunicación para control de iluminación.',
  PPM:
    'La señal codificada en pulsos que entrega un receptor de radiocontrol, que lleva varios canales por un solo hilo.',
};

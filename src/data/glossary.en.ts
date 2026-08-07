/**
 * L2 glossary. Transcribed verbatim from web/content/en/_common.md.
 *
 * The gloss is the content; the tooltip is only one possible presentation of
 * it. Every page reads correctly with the glosses removed, which is what
 * information-architecture.md section 6 rule 4 demands.
 *
 * Convention decided in P-16: a term is marked ONCE per page, on its first
 * occurrence. Marking every instance turns body copy into a minefield of
 * dotted underlines.
 */
export const GLOSSARY: Record<string, string> = {
  'bare metal':
    'Code that runs straight on the microcontroller, with no operating system underneath it.',
  pinout:
    'The assignment of each physical pin of a microcontroller to a function. Fixing it decides what the hardware and the software can each do.',
  HAL:
    'Hardware abstraction layer: the thin layer that lets the same application code run on a different microcontroller.',
  'Class B':
    'The category of safety-related software defined by the appliance safety standards. It prescribes what the software has to detect about its own failures, and how that has to be proven.',
  PEC:
    'Protective electronic circuit: hardware whose job is to take the appliance to a safe state when something fails.',
  'CB scheme':
    'An international arrangement under which a test report from one certification body is accepted by the others, instead of testing again per country.',
  'VDE, UL':
    'Certification bodies, German and American respectively, that assess and certify electrical products.',
  PID:
    'The standard feedback control law: it corrects using the current error, its accumulated history, and its rate of change.',
  FOPDT:
    'First order plus dead time: a simple mathematical model of how a slow physical system responds, used to tune a control loop before touching the real thing.',
  'cold junction compensation':
    'A thermocouple measures a difference in temperature, so to get an absolute reading you need the temperature at the other end of the wire, and you have to correct for it.',
  'V-Model':
    'A development process that pairs every specification step with the test that proves it.',
  ALM:
    'Application lifecycle management: the tooling that holds requirements, tasks, and tests in one traceable place.',
  'end of line':
    'The final test station on a production line, where every unit is checked before it ships.',
  'DALI, DMX': 'Standard communication protocols for lighting control.',
  PPM:
    'The pulse-coded signal a radio-control receiver puts out, carrying several channels on one wire.',
};

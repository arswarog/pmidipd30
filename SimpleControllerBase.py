from __future__ import with_statement

from ableton.v2.base import Slot
from ableton.v2.control_surface.control_surface import SimpleControlSurface
from ableton.v2.control_surface.input_control_element import \
    InputControlElement, MIDI_CC_TYPE, MIDI_NOTE_TYPE


class SimpleControllerBase(SimpleControlSurface):
  
  def __init__(self, c_instance):
    super(SimpleControllerBase, self).__init__(c_instance)
    with self.component_guard():
      self._setup()

  def _log_message(self, *msg):
    self._c_instance.log_message(
        '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, msg))))

  def _register_slider(self, callback, ctrl, ch = 0, is_cc = True):
    element = InputControlElement(
        MIDI_CC_TYPE if is_cc else MIDI_NOTE_TYPE, ch, ctrl)
    self.register_slot(element, callback, 'value')
    return element

  def _register_trigger(self, callback, ctrl, ch = 0, is_cc = True):
    return self._register_slider(lambda v: v and callback(), ctrl, ch, is_cc)

  def _register_listener(self, callback, subj, key):
    self.register_slot(Slot(subj, callback, key))

  def _setup(self):
    raise NotImplementedError('Override _setup to set up controllers.')

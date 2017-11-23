#-----------------------------------------------
#                        
#  Adapted from Keith McMillen's QuNexus.
#                        
#-----------------------------------------------

from __future__ import with_statement

import Live

from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.MixerComponent import MixerComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.ChannelStripComponent import release_control

class EnhancedMixerComponent(MixerComponent):
  def __init__(self, *a, **k):
    super(EnhancedMixerComponent, self).__init__(*a, **k)
    self._crossfader_left_button = None
    self._crossfader_right_button = None

  def disconnect(self):
    super(EnhancedMixerComponent, self).disconnect()
    release_control(self._crossfader_left_button)
    release_control(self._crossfader_right_button)
    self._crossfader_left_button = None
    self._crossfader_right_button = None

  def set_crossfader_buttons(self, left, right):
    release_control(self._crossfader_left_button)
    release_control(self._crossfader_right_button)
    self._crossfader_left_button = left
    self._crossfader_right_button = right
    self.update()

  def update(self):
    super(EnhancedMixerComponent, self).update()
    if self._allow_updates:
      master_track = self.song().master_track
      if self.is_enabled():
        if self._crossfader_left_button != None:
          self._crossfader_left_button.connect_to(
                  master_track.mixer_device.crossfader)
        if self._crossfader_right_button != None:
          self._crossfader_right_button.connect_to(
                  master_track.mixer_device.crossfader)
      else:
        release_control(self._crossfader_left_button)
        release_control(self._crossfader_right_button)
    else:
      self._update_requests += 1

class PMIDIPD30Ctrl(ControlSurface):
  __module__ = __name__
  __doc__ = "PMIDIPD30Ctrl controller script"
  
  def __init__(self, c_instance):
    ControlSurface.__init__(self, c_instance)
    with self.component_guard():
      self._setup_transport_control()
      self._setup_mixer_control()
    self.log_message("Created PMIDIPD30Ctrl.")

  def _setup_transport_control(self):
    self._transport = TransportComponent(play_toggle_model_transform = None)
    self._transport.set_record_button(ButtonElement(True, MIDI_CC_TYPE, 0, 44))
    self._transport.set_play_button(ButtonElement(True, MIDI_CC_TYPE, 0, 45))

  def _setup_mixer_control(self):
    self._mixer = EnhancedMixerComponent()
    self._mixer.set_crossfader_control(SliderElement(MIDI_CC_TYPE, 0, 9))
    self._mixer.set_crossfader_buttons(
            ButtonElement(True, MIDI_CC_TYPE, 0, 1),
            ButtonElement(True, MIDI_CC_TYPE, 0, 2))

  def disconnect(self):
    ControlSurface.disconnect(self)
    self.log_message("Closed PMIDIPD30Ctrl.")

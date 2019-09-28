"""CSC148 Assignment 1 - Making Music

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains classes that describe sound waves, instruments that play
these sounds and a function that plays multiple instruments simultaneously.

As discussed in the handout, you may not change any of the public behaviour 
(attributes, methods) given in the starter code, but you can definitely add 
new attributes, functions, classes and methods to complete your work here.

"""
from __future__ import annotations
import typing
import csv
import numpy
from helpers import play_sounds, make_sine_wave_array


class SimpleWave:
    """ Attributes:
    frequency: The frequency of the sound wave
    duration: The duration of the sound wave
    amplitude: the amplitude for the sound wave





    """
    frequency: int
    duration: float
    amplitude: float

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """
        initialize this simple sound program
         """
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def __eq__(self, other: SimpleWave) -> bool:
        """
        Give the information when two waves are equal
        >>> A = SimpleWave(400,400,1)
        >>> B = SimpleWave(400,400,1)
        >>> A == B
        True


        """
        return self.frequency == other.frequency and \
               self.duration == other.duration and self.amplitude \
               == other.amplitude

    def __ne__(self, other: SimpleWave) -> bool:
        """
        when two waves are not equal
        >>> A = SimpleWave(500,500,1)
        >>> B = SimpleWave(400,400,1)
        >>> A != B
        True

         """
        return not (self.frequency ==
                    other.frequency and
                    self.duration == other.duration and
                    self.amplitude
                    == other.amplitude)

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """
        adding two simple waves together

        """
        new_list = []
        if other is ComplexWave:
            new_list = [i for i in other.waves]
            new_list.append(self)
        else:
            new_list.append(self)
            new_list.append(other)
        return ComplexWave(new_list)

    def get_duration(self) -> float:
        """ Give the duration of the simplewave"""

        return self.duration

    def play(self) -> numpy.ndarray:
        """
        Make the sound..
         """
        song = make_sine_wave_array(self.frequency,
                                    self.duration)
        return song

    def get_waves(self) -> list:
        """helper """
        return [self]


class ComplexWave:
    """ attributes:
    waves: a list of simple wave

    this class could put the simple waves together



    """
    waves: list

    def __init__(self, waves: typing.List[SimpleWave]) -> None:
        """ information of the Complexwave """
        self.waves = waves

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Add up two Complex waves  """
        term = [i for i in self.waves]
        if isinstance(other, ComplexWave):
            term.extend(other.waves)
        else:
            term.append(other)
        return ComplexWave(term)

    def complexity(self) -> int:
        """ Give the Complexity of the wave
        """
        return len(self.waves)

    def play(self) -> numpy.ndarray:
        """ Make NOISE"""

        first_item = self.waves[0]
        sound = make_sine_wave_array(first_item.frequency,
                                     self.get_duration())
        for i in range(1, len(self.waves)):
            sound += make_sine_wave_array(self.waves[i].frequency,
                                          self.get_duration())

        ab_sound = abs(sound)
        if ab_sound != [] and max(ab_sound) > 1:
            return sound / max(ab_sound)
        else:
            return sound

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Give You Waves """
        lst = []
        for i in self.waves:
            lst.append(i)
        return lst

    def get_duration(self) -> float:
        """ As the name, give you the duration """
        total_duration = []
        for comp in self.waves:
            for i in comp.get_waves():
                total_duration.append(i.duration)
        return max(total_duration)


class SawtoothWave(ComplexWave):
    """ The special Type of Wave """

    frequency: int
    duration: float
    amplitude: float

    def __init__(self, fund_frequency: int, duration: float,
                 amplitude: float) -> None:
        """ Info of the class """
        waves = []
        self.frequency = fund_frequency
        self.duration = duration
        f = fund_frequency
        self.amplitude = amplitude
        a = amplitude
        for i in range(1, 11):
            f_here = round(i * f)
            a_here = a / i
            waves.append(SimpleWave(f_here,
                                    duration, a_here))
        super().__init__(waves)

    def __add__(self, other: ANYWAVE) -> ComplexWave:
        return super().__add__(other)

    def complexity(self) -> int:
        """ complexity of the wave """
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ Make Sound"""
        return super().play()

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Give you the waves"""
        return super().get_waves()

    def get_duration(self) -> float:
        """ give the duration """
        return super().get_duration()


class SquareWave(ComplexWave):
    """ Special wave"""
    frequency: int
    duration: float
    amplitude: float

    def __init__(self, fund_frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Info for the class"""
        self.frequency = fund_frequency
        self.duration = duration
        f = fund_frequency
        self.amplitude = amplitude
        a = amplitude
        waves = []
        for i in range(1, 11):
            f_here = (2 * i - 1) * f
            a_here = a / (2 * i - 1)
            waves.append(SimpleWave(f_here,
                                    duration, a_here))
        super().__init__(waves)

    def __add__(self, other: ANYWAVE) -> ComplexWave:
        return super().__add__(other)

    def complexity(self) -> int:
        """ Same as superclass """
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ play the wave """
        return super().play()

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Get waves"""
        return super().get_waves()

    def get_duration(self) -> float:
        """ get the duration """
        return super().get_duration()


class Rest(ComplexWave):
    """ Special wave class rest """
    duration: float

    def __init__(self,
                 duration: float) -> None:
        """ info of rest class """
        self.duration = duration
        super().__init__([SimpleWave(1, duration, 1)])

    def __add__(self, other: ANYWAVE) -> ComplexWave:
        return super().__add__(other)

    def complexity(self) -> int:
        """ complexity of the wave"""
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ play the rest wave """
        first_item = self.waves[0]
        sound = make_sine_wave_array(first_item.frequency,
                                     self.get_duration())
        for i in range(1, len(self.waves)):
            sound += make_sine_wave_array(self.waves[i].frequency,
                                          self.get_duration())
        return sound * 0

    def get_waves(self) -> typing.List[SimpleWave]:
        """ get the waves """
        return super().get_waves()

    def get_duration(self) -> float:
        """ give the duration """
        return super().get_duration()


class Note:
    """ Class note.  """
    amplitude: float
    waves: list

    def __init__(self, waves: typing.List[ANYWAVE]) -> None:
        """ info of the class"""
        self.waves = waves
        self.amplitude = 1

    def __add__(self, other: Note) -> Note:
        """ add two notes together"""
        term = [i for i in self.waves]
        term.extend(other.waves)
        new_amplitude = max(self.amplitude, other.amplitude)
        to_return = Note(term)
        to_return.amplitude = new_amplitude
        return to_return

    def get_waves(self) -> typing.List[ANYWAVE]:
        """ give the waves"""
        lst = []
        for i in self.waves:
            lst.append(i)
        return lst

    def get_duration(self) -> float:
        """ return the duration """
        total_duration = []
        for i in self.waves:
            total_duration.append(i.get_duration())
        return sum(total_duration)

    def play(self) -> numpy.ndarray:
        """ play the nparray(wave)"""
        final = self.waves[0].play() * self.amplitude
        for i in range(1, len(self.waves)):
            final = numpy.hstack((final, self.waves[i].play() *
                                  self.amplitude))
        return final


class StutterNote(Note):
    """ Sepcial Note"""
    amplitude: float
    duration: float
    frequency: int

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ give the info of the class"""
        waves = []
        dur = duration * 1000
        count = 0
        while dur >= 25:
            if count % 2 == 0:
                waves.append(SawtoothWave(frequency,
                                          0.025, amplitude))
            else:
                waves.append(Rest(0.025))
            count += 1
            dur -= 25

        if dur != 0:
            waves.append(Rest(dur / 1000))

        super().__init__(waves)
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def __add__(self, other: ANYWAVE) -> Note:
        """ add two special notes together"""
        return super().__add__(other)

    def get_waves(self) -> typing.List[ANYWAVE]:
        return super().get_waves()

    def get_duration(self) -> float:
        """ get the duration """
        total_duration = []
        for i in self.waves:
            total_duration.append(i.duration)

        return float(sum(total_duration))

    def play(self) -> numpy.ndarray:
        """ play the special note """
        return super().play()


class Instrument:
    """Class of instrument"""
    own_note: Note

    def __init__(self) -> None:
        self.own_note = Note([])

    def get_duration(self) -> float:
        """Get the duration """
        return self.own_note.get_duration()

    def change_own_note(self, note: Note) -> None:
        """ Helper function."""
        self.own_note = note

    def play(self) -> numpy.ndarray:
        """ play the instrument sound. """
        return self.own_note.play()

    def get_own_note(self) -> Note:
        """Helper function """
        return self.own_note


class Baliset(Instrument):
    """ Instrument class. """
    own_note: Note
    fundamental_frequency: int

    def __init__(self) -> None:
        """ info,"""
        super().__init__()
        self.fundamental_frequency = 196

    def get_duration(self) -> float:
        """ give the duration that instrument play"""
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str,
                                                       float, float]]
                   ) -> None:
        """ give you the next note  """
        final_wave = []
        for i in note_info:
            type_require = i[0]
            if type_require == "rest":
                final_wave.append(Rest(i[2]))
            else:
                freq = type_require.split(":")
                frequency = self.fundamental_frequency * \
                            int(freq[0]) / int(freq[1])
                final_wave.append(SawtoothWave(int(frequency),
                                               i[2], i[1]))
        self.change_own_note(Note(final_wave))

    def play(self) -> numpy.ndarray:
        """ play by instrument"""
        return super().play()


class Holophonor(Instrument):
    """ A instrument """
    fundamental_frequency: int

    def __init__(self) -> None:
        """ info for the instrument """
        super().__init__()
        self.fundamental_frequency = 65

    def get_duration(self) -> float:
        """ How long the instrument play """
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float,
                                                       float]]
                   ) -> None:
        """ go the to next note """
        # get the first note
        type_require = note_info[0][0]
        if type_require == "rest":
            final_note = Note(Rest(note_info[0][2]).get_waves())
        else:
            freq = type_require.split(":")
            frequency = self.fundamental_frequency * int(freq[0]) / \
                        int(freq[1])
            final_note = StutterNote(int(frequency),
                                     note_info[0][2], note_info[0][1])
        # get the rest notes
        for i in note_info[1:]:
            type_require = i[0]
            if type_require == "rest":
                final_note += Note(Rest(i[2]).get_waves())
            else:
                freq = type_require.split(":")
                frequency = self.fundamental_frequency * \
                            int(freq[0]) / int(freq[1])
                final_note += StutterNote(int(frequency), i[2], i[1])
        self.change_own_note(final_note)

    def play(self) -> numpy.ndarray:
        """ play the instrument """
        return super().play()


class Gaffophone(Instrument):
    """ Gaffophone Instrument"""
    fundamental_frequency: int

    def __init__(self) -> None:
        """ info of the class """
        super().__init__()
        self.fundamental_frequency = 131

    def get_duration(self) -> float:
        """ How long that instrument should play"""
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ play the next note  """
        final_wave = []
        for i in note_info:
            type_require = i[0]
            if type_require == "rest":
                final_wave.append(Rest(i[2]))
            else:
                freq = type_require.split(":")
                frequency = self.fundamental_frequency * \
                            int(freq[0]) / int(freq[1])
                mediate_wave = SquareWave(int(frequency), i[2], i[1]) + \
                               SquareWave(int(frequency * 3 / 2), i[2], i[1])
                final_wave.append(mediate_wave)
        self.change_own_note(Note(final_wave))

    def play(self) -> numpy.ndarray:
        """ play the instrument """
        return super().play()

    def get_own_note(self) -> Note:
        return super().get_own_note()


def play_song(song_file: str, beat: float) -> None:
    """ Read the fking  song file and play it  """
    with open(song_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        total_list = []
        count = 0
        for row in spamreader:
            if count == 0:
                total_list = _get_instruments(row, total_list)
                count += 1
            else:
                total_list = _get_raw_notes(row, total_list)
        # figure out each note based on note_info
        for ins_list in total_list:
            note_list = []
            note_info_standby = []
            for raw in ins_list[1]:
                previous_duration = _cal_previous_duration \
                    (note_info_standby,
                     beat)
                if previous_duration > 1:
                    draft_each_note_list = \
                        _deal_with_irregular_notes(note_info_standby,
                                                   beat)
                    note_info_standby = _add_raw(raw, note_info_standby)
                elif raw != "":
                    this_note = raw.split(":")
                    # calculate durations
                    total_duration = float(this_note[-1]) * beat
                    # previous_duration = _cal_previous_duration \
                    #     (note_info_standby,
                    #      beat)
                    total_duration += previous_duration
                    draft_each_note_list = \
                        _deal_with_regular_notes(total_duration,
                                                 note_info_standby,
                                                 previous_duration,
                                                 beat, this_note)
                else:
                    draft_each_note_list = _add_rest_to_empty \
                        (note_info_standby,
                         beat)

                # if we fill in notes info in the draft list,
                # add it to note_list
                if draft_each_note_list:
                    note_list.append(draft_each_note_list)

            # add the note_list to ins_list once finish going over the raw_list
            ins_list.append(note_list)

        # try to play music now
        _play_music(total_list)


def _get_instruments(from_list: list, to_list: list) -> list:
    instruments = from_list[0].split(",")
    for ins in instruments:
        ins_list = [ins]
        raw_list = []
        ins_list.append(raw_list)
        to_list.append(ins_list)
    return to_list


def _get_raw_notes(from_list: list, to_list: list) -> list:
    temp = from_list[0].split(",")
    # figure out note_info for all instruments
    for i in range(len(to_list)):
        raw_list = to_list[i][1]
        raw_list.append(temp[i])
    return to_list


def _play_music(from_list: list) -> None:
    max_length = min([len(ins_list[2]) for ins_list
                      in from_list])
    for k in range(max_length):
        sound_list = _get_pending_sounds(from_list, k)
        play_sounds(sound_list)


def _get_pending_sounds(from_list: list, param: int) -> list:
    sound_list = []
    for ins_list in from_list:
        note_list = ins_list[2]
        if param < len(note_list):
            # choose an instrument to play
            if ins_list[0] == "Baliset":
                bali = Baliset()
                bali.next_notes(note_list[param])
                sound_list.append(bali)
            elif ins_list[0] == "Holophonor":
                holo = Holophonor()
                holo.next_notes(note_list[param])
                sound_list.append(holo)
            elif ins_list[0] == "Gaffophone":
                gaffo = Gaffophone()
                gaffo.next_notes(note_list[param])
                sound_list.append(gaffo)
    return sound_list


def _add_rest_to_empty(from_list: list, beat: float) -> list:
    draft_each_note_list = []
    previous_duration = 0
    if from_list:
        for note_standby in from_list:
            previous_duration += (float(note_standby[-1]) * beat)
    duration_needed = 1 - previous_duration
    for note_standby in from_list:
        # check type for standby notes
        if note_standby[0] == "rest":
            draft_each_note_list.append((note_standby[0], 1,
                                         float(note_standby[1]) * beat))
        else:
            draft_each_note_list.append((":".join(note_standby[:2]),
                                         float(note_standby[2]),
                                         float(note_standby[3]) * beat))
    draft_each_note_list.append(("rest", 1, duration_needed))
    return draft_each_note_list


def _cal_previous_duration(from_list: list, beat: float) -> float:
    previous_duration = 0
    if from_list:
        for note_standby in from_list:
            previous_duration += (float(note_standby[-1]) *
                                  beat)
    return previous_duration


def _add_previous_note(from_list: list, beat: float,
                       to_list: list) -> list:
    if from_list:
        for note_standby in from_list:
            # check type for standby notes
            if note_standby[0] == "rest":
                to_list.append((note_standby[0], 1,
                                float(note_standby[1]) * beat))
            else:
                to_list.append((":".join(note_standby[:2]),
                                float(note_standby[2]),
                                float(note_standby[3]) * beat))
    return to_list


def _add_current_note(from_list: list, to_list: list, beat: float,
                      duration: float) -> list:
    if from_list[0] == "rest":
        if duration == 0:
            duration = float(from_list[1]) * beat
        to_list.append((from_list[0], 1, duration))
    else:
        if duration == 0:
            duration = float(from_list[3]) * beat
        to_list.append((":".join(from_list[:2]), float(from_list[2]),
                        duration))
    return to_list


def _deal_with_regular_notes(total_duration: float, note_info_standby: list,
                             previous_duration: float,
                             beat: float, this_note: list) -> list:
    draft_each_note_list = []
    # deal with the note infos
    if total_duration < 1:
        note_info_standby.append(this_note)
    elif total_duration > 1:
        duration_needed = 1 - previous_duration
        draft_each_note_list = _add_previous_note(note_info_standby,
                                                  beat, draft_each_note_list)
        note_info_standby.clear()

        # spilt current note
        note_temp = this_note[:-1]
        note_temp.append((float(this_note[-1]) * beat - duration_needed) / beat)
        note_info_standby.append(note_temp)

        # check type for current note
        draft_each_note_list = _add_current_note(this_note,
                                                 draft_each_note_list,
                                                 beat,
                                                 duration_needed)
    else:
        draft_each_note_list = _add_previous_note(note_info_standby,
                                                  beat,
                                                  draft_each_note_list)
        note_info_standby.clear()

        # check type for current note
        draft_each_note_list = _add_current_note(this_note,
                                                 draft_each_note_list,
                                                 beat, 0)
    return draft_each_note_list


def _deal_with_irregular_notes(note_info_standby: list, beat: float) -> list:
    draft_each_note_list = []
    duration_count = 0
    to_continue = True
    pending_notes = []
    while to_continue:
        this_pend_note = note_info_standby.pop(0)
        this_pend_duration = float(this_pend_note[-1]) * beat
        duration_count += this_pend_duration
        if duration_count > 1:
            to_continue = False
            draft_each_note_list = _add_previous_note \
                (pending_notes, beat, draft_each_note_list)
            # spilt current note
            duration_needed = 1 - _cal_previous_duration(pending_notes, beat)
            note_temp = this_pend_note[:-1]
            note_temp.append((float
                              (this_pend_note[-1])
                              * beat - duration_needed) / beat)
            note_info_standby.insert(0, note_temp)

            # check type for current note
            draft_each_note_list = _add_current_note(this_pend_note,
                                                     draft_each_note_list,
                                                     beat,
                                                     duration_needed)
        elif duration_count == 1:
            to_continue = False
            draft_each_note_list = _add_previous_note(pending_notes, beat,
                                                      draft_each_note_list)
            draft_each_note_list = _add_current_note(this_pend_note,
                                                     draft_each_note_list,
                                                     beat, 0)
        else:
            pending_notes.append(this_pend_note)
    return draft_each_note_list


def _add_raw(raw: str, note_info_standby: list) -> list:
    if raw != "":
        note_info_standby.append(raw.split(":"))
    return note_info_standby


# This is a custom type for type annotations that
# refers to any of the following classes (do not 
# change this code)
ANYWAVE = typing.TypeVar('ANYWAVE',
                         SimpleWave,
                         ComplexWave,
                         SawtoothWave,
                         SquareWave,
                         Rest)

if __name__ == '__main__':
    play_song('/Users/duncan/Downloads/swan_lake.csv', 0.2)
    # import python_ta
    #
    # python_ta.check_all(config={'extra-imports': ['helpers',
    #                                               'typing',
    #                                               'csv',
    #                                               'numpy'],
    #                             'disable': ['E9997']})

# ##########################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# http://flatcam.org                                       #
# File Author: Matthieu Berthomé (Optimized version)       #
# Düzeltme: TB2EOS - 2026                                  #
# MIT Licence                                              #
# ##########################################################

from appPreProcessor import *


class GRBL_laser(PreProc):

    include_header = True
    coordinate_format = "%.*f"
    feedrate_format = '%.*f'

    # Lazer modu:
    #   'M04' = Dinamik güç (önerilen; hız düşünce güç de düşer, köşelerde yanık olmaz)
    #   'M03' = Sabit güç
    LASER_ON = 'M04'

    @staticmethod
    def _power(p):
        # Dönüş hızı alanı = lazer gücü (S). Boşsa 0 kabul et (SNone hatasını önler).
        try:
            s = p['spindlespeed']
            if s is None or s == '':
                return 0
            return int(float(s))
        except (ValueError, TypeError, KeyError):
            return 0

    def start_code(self, p):
        units = ' ' + str(p['units']).lower()
        power = self._power(p)
        gcode = '(Optimized GRBL Laser Postprocessor - TB2EOS)\n'
        gcode += '(GRBL lazer modu acik olmali: $32=1)\n\n'

        xmin = '%.*f' % (p.coords_decimals, p['options']['xmin'])
        xmax = '%.*f' % (p.coords_decimals, p['options']['xmax'])
        ymin = '%.*f' % (p.coords_decimals, p['options']['ymin'])
        ymax = '%.*f' % (p.coords_decimals, p['options']['ymax'])

        gcode += '(Feedrate: ' + str(p['feedrate']) + units + '/min' + ')\n'
        gcode += '(Feedrate rapids: ' + str(p['feedrate_rapid']) + units + '/min' + ')\n'
        gcode += '(Laser Power S: ' + str(power) + ')\n'
        gcode += '(Laser Mode: ' + self.LASER_ON + ')\n'
        if power == 0:
            gcode += '(UYARI: Lazer gucu 0 - Donus hizi alanina guc degeri girin!)\n'
        gcode += '(X range: ' + '{: >9s}'.format(xmin) + ' ... ' + '{: >9s}'.format(xmax) + ' ' + units + ')\n'
        gcode += '(Y range: ' + '{: >9s}'.format(ymin) + ' ... ' + '{: >9s}'.format(ymax) + ' ' + units + ')\n\n'

        # Güvenlik ve kurulum
        gcode += 'M05 S%d\n' % power  # Lazer kapalıyken gücü ayarla
        gcode += ('G20' if p.units.upper() == 'IN' else 'G21') + "\n"
        gcode += 'G90\n'
        gcode += 'G17\n'
        gcode += 'G94\n'
        gcode += 'F' + self.feedrate_format % (p.fr_decimals, p.feedrate) + '\n'

        return gcode

    def startz_code(self, p):
        return ''

    def lift_code(self, p):
        # Kalkış = lazeri kapat
        return 'M05'

    def down_code(self, p):
        # İniş = lazeri aç (S tekrar yazılır, güvenli)
        return '%s S%d' % (self.LASER_ON, self._power(p))

    def toolchange_code(self, p):
        return ''

    def up_to_zero_code(self, p):
        return 'M05'

    def position_code(self, p):
        return ('X' + self.coordinate_format + ' Y' + self.coordinate_format) % \
               (p.coords_decimals, p.x, p.coords_decimals, p.y)

    def rapid_code(self, p):
        return 'G00 ' + self.position_code(p)

    def linear_code(self, p):
        return 'G01 ' + self.position_code(p)

    def end_code(self, p):
        coords_xy = p['xy_end']
        gcode = 'M05\n'

        if coords_xy and coords_xy != '':
            gcode += 'G00 X%.*f Y%.*f\n' % (p.coords_decimals, float(coords_xy[0]),
                                           p.coords_decimals, float(coords_xy[1]))

        gcode += 'M30\n'
        return gcode

    def feedrate_code(self, p):
        # Her kesime inişte hız tekrar yazılır (farklı hızlı uçlar için doğru çalışır)
        return 'F' + self.feedrate_format % (p.fr_decimals, p.feedrate)

    def z_feedrate_code(self, p):
        return ''

    def spindle_code(self, p):
        return '%s S%d' % (self.LASER_ON, self._power(p))

    def dwell_code(self, p):
        return ''

    def spindle_stop_code(self, p):
        return 'M05'

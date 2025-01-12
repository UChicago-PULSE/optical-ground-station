import datetime
from zoneinfo import ZoneInfo

from nexstar_control.device import NexStarHandControl, TrackingMode, LatitudeDMS, LongitudeDMS

hc = NexStarHandControl('/dev/tty.PL2303G-USBtoUART110')
if not hc.is_connected():
    print("Failed to connect to device")
    exit(1)

# get the current position of the telescope in ra/dec or alt/az coordinates
ra, dec = hc.get_position_ra_dec()
alt, az = hc.get_position_alt_az()

# issue go to commands in ra/dec coordinates or alt/az coordinates
hc.goto_ra_dec(180, 0)
hc.goto_alt_az(90, 0)

# turn the telescope tracking mode off when doing slewing, but save the current mode to restore later
current_tracking_mode = hc.get_tracking_mode()
hc.set_tracking_mode(TrackingMode.OFF)

# slew the telescope at fixed rates (where negative values indicate the opposite direction)
hc.slew_fixed(9, -9)

# slew the telescope at variable rates (where negative values indicate the opposite direction)
hc.slew_variable(15000, -15000)

# restore the tracking mode
hc.set_tracking_mode(current_tracking_mode)

# set the location and time of the telescope
hc.set_location(lat=LatitudeDMS.from_decimal(49.2849), lng=LongitudeDMS.from_decimal(-122.8678))
dt = datetime.datetime.now(tz=ZoneInfo("America/Vancouver"))
hc.set_time(dt)
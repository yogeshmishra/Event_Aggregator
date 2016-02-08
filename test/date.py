import timestring 
dte = timestring.Date('27 Mar 2014 12:32:29 PST')
print "sdsd" , dte
print "s", dte.tzname


from calendar import timegm
from datetime import datetime, timedelta, tzinfo
from email.utils import parsedate_tz

ZERO = timedelta(0)
time_string = 'Mon, 16 Nov 2009 13:32:02 +0100'
tt = parsedate_tz(time_string)
#NOTE: mktime_tz is broken on Python < 2.7.4,
#  see https://bugs.python.org/issue21267
timestamp = timegm(tt) - tt[9] # local time - utc offset == utc time
naive_utc_dt = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
aware_utc_dt = naive_utc_dt.replace(tzinfo=FixedOffset(ZERO, 'UTC'))
aware_dt = aware_utc_dt.astimezone(FixedOffset(timedelta(seconds=tt[9])))
print(aware_utc_dt)
print(aware_dt)

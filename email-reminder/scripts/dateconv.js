function renderDate(year, month, day, hours, minutes) {
    var myDate = new Date(Date.UTC(year, month, day, hours, minutes));
    return myDate.toString();
    }

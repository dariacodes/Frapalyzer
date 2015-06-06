(function() {
    var a = $.map($('li'), function(e) {
        var arr = $(e).text().toLowerCase().trim().split(' pour ');
        return { 's' : arr[0], 'f' : arr[1] };
    });
    a.splice(a.indexOf($.grep(a, function(i) { return i.s === 'zoo'; })[0])+1);
    return JSON.stringify(a);
})()
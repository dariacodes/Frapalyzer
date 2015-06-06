JSON.stringify($.map($("div[id^=art]"), function (art) {
    try {
        var $art = $(art)
          , mot = $($art.children('.tlf_cmot')[0]).text().replace(/[.,\s]+$/, "").toLowerCase().trim()
          , def = $($art.children('.tlf_cdefinition')[0]).text()
               || $art.text().replace(/^.*? \(de ([^)]+?)\).*$/, "$1");
        return !mot ?
               null :
               { apo: mot, full: def.replace(/\([^)]+\)/g, "").replace(/[.,\s]+$/, "").toLowerCase().trim() };
    } catch(e) { return null; }
}))
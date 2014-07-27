//New Abbrase module
var abbrasePassphraseGen = function () {
    var unigrams, prefixes

    var ADJ = 0, NOUN = 1, VERB = 2

    function generate(length) {
        /* pick series of prefixes that will make up the passwords (Ryan Hitchman) */
        var numbers = new Uint16Array(length)
        getRandoms(numbers)

        //parts of speech: [adjectives] + noun + verb + [adjectives] + noun
        var noun = Math.floor((length - 3) / 2)
        var words = []

        for (var i = 0; i < length; i++) {
            var pre = prefixes[numbers[i] % 1024]
            var pos = ADJ
            if(i === noun || i === length - 1)
                pos = NOUN
            else if(i === noun + 1)
                pos = VERB
            words[i] = pre + getWordForPrefix(unigrams[pre], pos)
        }
        return words
    }

    function getRandoms(arr) {
        if (window.polyfilledCrypto) {
            //polyfill should overwrite Math.random()
            for (var i = 0; i < arr.length; i++) {
                arr[i] = Math.floor(Math.random() * 1024)
            }
        } else crypto.getRandomValues(arr)
    }

    function getWordForPrefix(prefix, pos) {
        if(prefix[pos].length)
            return choice(prefix[pos])
        else {
            //No words of the right type for this prefix :(
            var words = []
            for (var i = 0; i < prefix.length; i++) {
                for (var j = 0; j < prefix[i].length; j++) {
                    words.push(prefix[i][j])
                }
            }
            return choice(words)
        }
    }

    //pseudo-random as we're just choosing which suffix to use
    function choice(arr) {
        return arr[Math.floor(Math.random() * arr.length)]
    }

    return {
        generate: generate,
        load: function (json) {
            unigrams = json
            prefixes = Object.keys(unigrams)
        }
    }
}()
//End abbrase module

function show_phrase() {
    var length = Number($('#wordcount').val());
    if(!length || length < 3 || length > 10){
        length = 5
        $('#wordcount').val(5)
    }
    var words = abbrasePassphraseGen.generate(length),
        container = $('.current'),
        phrase = '', abbrase = ''
    for (var i = 0; i < length; i++) {
        var abbr = words[i].substring(0,3)
        var span = '<span>' + abbr + '</span>'
        phrase += span + words[i].substring(3) + ' '
        abbrase += span
    }

    var oldphrase = container.find('.phrase').html(),
        oldabbrase = container.find('.abbrase').html()
    $phrase = $('<div><span class="phrase">' + oldphrase + '</span></div>')
    $abbrase = $('<span class="abbrase">' + oldabbrase + '</span>').click(selectThis).prependTo($phrase)
    $('.history').prepend($phrase)

    container.find('.phrase').html(phrase)
    container.find('.abbrase').html(abbrase)
}

$.ajaxSetup({
    cache: true
})

function rngPolyfill() {
    //Check copied from Modernizr
    if ('crypto' in window && !!window.crypto && 'getRandomValues' in window.crypto)
        return true
    window.polyfilledCrypto  = true
    return $.getScript('//cdnjs.cloudflare.com/ajax/libs/seedrandom/2.3.6/seedrandom.min.js').then(function () {
        Math.seedrandom()
    })
}


var ready = $.Deferred()
$.when($.ajax({dataType: "json", url: 'unigrams.json'}), rngPolyfill(), ready)
    .done(function (response) {
        abbrasePassphraseGen.load(response[0])
        for (var i = 0; i < 12; i++) {
            show_phrase()
        }
        $('p.abbrase').attr('title', 'Your new password')
        $('.history div').last().prepend($('<div class="example">Example (do not use):</div>'))
        $('.abbrase').click(selectThis)
        $('#wordcount').change(show_phrase)
        $('.btn').click(function() {
            show_phrase()
            return false
        })
})

$(document).ready(function () {
    $('.btn').click(function () {return false})
    ready.resolve()
})

function selectThis() {
    //MDN
    var sel = window.getSelection()
    if (sel.isCollapsed) {
        var range = document.createRange()
        range.setStartBefore(this.firstChild)
        range.setEndAfter(this.lastChild)
        sel.removeAllRanges()
        sel.addRange(range)
    }
}
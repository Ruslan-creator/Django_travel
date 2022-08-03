window.onload = () => {
    let q, range, stars
    const input_rating = $('#rating')
    const low_price = $('#low_price')
    const high_price = $('#high_price')
    const q_search = $('#q-search')
    const search_btn = $('#search-btn')

    //amm session
    const ammStars = sessionStorage.getItem('amm-stars')
    const ammRange = sessionStorage.getItem('amm-range')
    const ammQ = sessionStorage.getItem('amm-q')
    if (ammStars) {
        stars = Number(ammStars)
        input_rating.val(stars)
        $(`[data-star="${stars}"]`).addClass('active')
    }

    $('.sltru-start').on('click', function () {
        let clickedStar = $(this).attr('data-star')
        if (clickedStar > 0) {
            clickedStar = Number(clickedStar)
            console.log(clickedStar, 'clicked start')
            const target = $(`[data-star="${clickedStar}"]`)
            let prevTarget = $(`[data-star="${stars}"]`)
            if (stars) {
                prevTarget = $(`[data-star="${stars}"]`)
            }
            if (target.hasClass('active')) {
                target.removeClass('active')
                stars = null
            } else {
                prevTarget.removeClass('active')
                target.addClass('active')
                stars = clickedStar
            }
        }
    })

    search_btn.on('click', () => {
        // stars
        input_rating.val(stars || '');
        if (stars) {
            sessionStorage.setItem('amm-stars', stars)
        } else {
            sessionStorage.removeItem('amm-stars')
        }
        // stars end
        //range
        if (range) {
            const array = range.split(',')
            if (array && array.length) {
                const l = array[0]
                const h = array[1]
                low_price.val(h || 0)
                high_price.val(l || 0)
                sessionStorage.setItem('amm-range', range)
            }
        }
        //range end
        //qsearch
        if (q) {
            alert(value)
            if (value && q) {
                sessionStorage.setItem('amm-q', q)
            }
        }
        //qsearch end
    })

    q_search.on('change', (e) => {
        q = e.target.value
    })

    $('.range-slider').jRange({
        from: 0,
        to: 10000,
        step: 1,
        format: '%s',
        width: 300,
        showLabels: true,
        isRange: true,
        onstatechange: (e) => {
            range = e
            console.log(range, 'range')
        }
    });
    setTimeout(() => {
        if (ammRange) {
            range = ammRange
            $('.range-slider').jRange('setValue', range || '10, 20');
        }
    }, 100)

    console.warn(ammQ, 'ammQ')
    if (ammQ) {
        console.warn(ammQ, 'ammQ111111')
        q = ammQ
        q_search.val(ammQ)
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var scrollFooter = document.getElementById('scroll-footer');
    var lastScrollTop = 0;

    window.addEventListener("scroll", function () {
        var st = window.scrollY;

        if (st > lastScrollTop) {
            // Scroll down
            scrollFooter.classList.add('show');
        } else {
            // Scroll up
            scrollFooter.classList.remove('show');
        }

        lastScrollTop = st <= 0 ? 0 : st;
    });
});

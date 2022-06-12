const toggleForm = () => {
    const container = document.querySelector('.containers');
    container.classList.toggle('active');
};

$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 40,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 4
        }
    }
})

$('.card_img').owlCarousel({
    loop: true,
    margin: 40,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
})

$('.owl-carousel-itinerary').owlCarousel({
    loop: true,
    margin: 40,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000,
    responsive: {
        0: {},
        600: {
            items: 3
        },
        1000: {
            items: 4
        }
    }
})

// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("myHeader");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}
$( document ).ready(function() {
    $('#drpcontinent').on('change',function() {
        $('.ddcnt').hide();
        $('#drpcountry').hide();
        if ($('#drpcountry li').hasClass(this.value)) {
            $(`.${this.value}`).show();
            $('#drpcountry').show();
        }else{
            $('.ddcnt').hide();
            $('#drpcountry').hide();
        }
    });
});
setTimeout(() => {
    $('#loader').addClass('d-none');
    $('#mainwrap').css('display','block');
}, 1500);
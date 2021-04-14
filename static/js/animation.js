$(document).ready(function () {
  $(".landing-anime").waypoint(
    function (direction) {
      $(".landing-anime").addClass(
        "animate__animated animate__fadeIn animate__delay-1s"
      );
    },
    {
      offset: "50%",
    }
  );

  $(".services-anime").waypoint(
    function (direction) {
      $(".services-anime").addClass("animate__animated animate__zoomIn");
    },
    {
      offset: "50%",
    }
  );

  $(".achievement-anime").waypoint(
    function (direction) {
      $(".achievement-anime").addClass(
        "animate__animated animate__fadeInLeftBig"
      );
    },
    {
      offset: "50%",
    }
  );

  $(".loans-anime").waypoint(
    function (direction) {
      $(".loans-anime").addClass("animate__animated animate__zoomIn");
    },
    {
      offset: "50%",
    }
  );

  $(".steps-anime").waypoint(
    function (direction) {
      $(".steps-anime").addClass("animate__animated animate__zoomIn");
    },
    {
      offset: "50%",
    }
  );

  $(".cal-anime").waypoint(
    function (direction) {
      $(".cal-anime").addClass("animate__animated animate__fadeInRightBig");
    },
    {
      offset: "50%",
    }
  );

  $(".faq-anime").waypoint(
    function (direction) {
      $(".faq-anime").addClass("animate__animated animate__zoomIn");
    },
    {
      offset: "50%",
    }
  );

  $(".counter-anime").waypoint(
    function (direction) {
      $(".counter-anime").addClass("animate__animated animate__zoomInUp");
    },
    {
      offset: "50%",
    }
  );

  $(".testimonial-anime").waypoint(
    function (direction) {
      $(".testimonial-anime").addClass("animate__animated animate__zoomIn");
    },
    {
      offset: "50%",
    }
  );

  $(".footer-anime").waypoint(
    function (direction) {
      $(".footer-anime").addClass("animate__animated animate__fadeIn");
    },
    {
      offset: "50%",
    }
  );

  $(".text-anime-landing").waypoint(
    function (direction) {
      $(".text-anime-landing").addClass("animate__animated animate__fadeIn");
    },
    {
      offset: "50%",
    }
  );

  $(".text-anime-loans").waypoint(
    function (direction) {
      $(".text-anime-loans").addClass("animate__animated animate__fadeIn");
    },
    {
      offset: "50%",
    }
  );

  $(".text-anime-steps").waypoint(
    function (direction) {
      $(".text-anime-steps").addClass("animate__animated animate__fadeIn");
    },
    {
      offset: "50%",
    }
  );

  $(".text-anime-cal").waypoint(
    function (direction) {
      $(".text-anime-cal").addClass("animate__animated animate__fadeIn");
    },
    {
      offset: "50%",
    }
  );

  $(".text-anime-testimonial").waypoint(
    function (direction) {
      $(".text-anime-testimonial").addClass(
        "animate__animated animate__fadeIn"
      );
    },
    {
      offset: "50%",
    }
  );
});

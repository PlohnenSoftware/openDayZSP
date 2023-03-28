{
  //loading screen
  let loadingScreen = function () {
      $(window).on("load", function () {
          $(".loader-wrapper").fadeOut("slow");
      });
  };

  // Search Bar
  let redirFu = function () {
      window.location.replace("../" + $("#webSearchInput").val());
      $(".loader-wrapper").fadeIn("slow");
  };

  let searchBar = () => {
      document.querySelector("#webSearchInput").addEventListener("keypress", (e) => {
          if (e.key === "Enter") {
              redirFu();
          }
      });
      document.querySelector(".web-search-submit").addEventListener("click", redirFu);
  };
  
  //paypal
  let paypalBar = async function () {
      PayPal.Donation.Button({
          env: "production",
          hosted_button_id: "948Y2AG949RVY",
          image: {
              src: "https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif",
              alt: "Donate with PayPal button",
              title: "PayPal - The safer, easier way to pay online!",
          },
      }).render("#donateButton");
  };

  //onload
  $(document).ready(() => {
      searchBar();
      paypalBar();
      loadingScreen();
  });
}

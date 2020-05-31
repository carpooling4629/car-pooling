/**
 * Created by LUCIFER td on 28-03-2020.
 */

    var firebaseConfig = {
    apiKey: "AIzaSyBvYy92lzJ7CtI7vdCqHjO5zrQJB0_Gp3I",
    authDomain: "live-tracking-b8bfb.firebaseapp.com",
    databaseURL: "https://live-tracking-b8bfb.firebaseio.com",
    projectId: "live-tracking-b8bfb",
    storageBucket: "live-tracking-b8bfb.appspot.com",
    messagingSenderId: "203218377661",
    appId: "1:203218377661:web:16adc99f0ea968cf6750d4",
    measurementId: "G-BEV51G020G"
  };
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
    var db = firebase.database().ref('/');
    var tracker;
function check(rollno) {
    var status;
    db.once('value', function (snapshot) {
           var gh = snapshot.val();
           status= (gh[rollno].status);
      if(status==1)
      {
          console.log("hh");
                var clat,clng,plat=0,plng=0;
                if (navigator.geolocation)
                    {
                        tracker= setInterval(function(){
                            navigator.geolocation.getCurrentPosition(function (p) {
                            // clat = p.coords.latitude;
                            // clng = p.coords.longitude;

                                        clat = p.coords.latitude;
                                        clng = p.coords.longitude;
                                        var d = {};
                               var ltln = {
                                          lat:clat,
                                          lng:clng,
                                          status:status
                                        };
                               d[rollno] = ltln;
                               db.update(d);
                               console.log(ltln);
                            });
                        }, 1000);
                    }
                else
                {
                    alert('Geo Location feature is not supported in this browser.');
                }
      }
      else
      {
          clearInterval(tracker);
      }
});
  }

  function enable(rollno) {
              var d = {};
              var ltln = {
                  status: 1
              };
              d[rollno] = ltln;
              db.update(d);
  }
  function disable(rollno) {
          var d = {};
            var ltln = {
              status:0
            };
            d[rollno] = ltln;
            db.update(d);
            clearInterval(tracker);
            console.log(tracker,"cleared");
  }
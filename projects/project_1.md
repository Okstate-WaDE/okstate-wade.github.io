---
---

<div class="content">

	<section>
		<div class="container flex">
             <div id="map">
            <style type="text/css">
              #map {
                  width:400px;
                  height:550px;
                  <!--background-color: red;-->
                }
            </style>
             </div>
             <script>
                 var map = L.map('map').setView([51.505, -0.09], 13);
                 L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                     maxZoom: 19,
                     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                 }).addTo(map);
                 var transitions = new L.tileLayer("https://storage.googleapis.com/global-surface-water/tiles2021/transitions/{z}/{x}/{y}.png",
                     { format: "image/png",
                           maxZoom: 13,
                           errorTileUrl : "https://storage.googleapis.com/global-surface-water/downloads_ancillary/blank.png",
                           attribution: "2016 EC JRC/Google" });
                     map.addLayer(transitions);
                 </script>
		</div>
	</section>

</div>

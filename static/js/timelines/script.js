<script src="../static/js/timeline/script.js" type="text/javascript"></script>
var tl;
function onLoad() {
  var eventSource = new Timeline.DefaultEventSource();
  var bandInfos = [
    Timeline.createBandInfo({
		eventSource:    eventSource,
        width:          "75%", 
        intervalUnit:   Timeline.DateTime.DAY, 
        intervalPixels: 300
    }),
    Timeline.createBandInfo({
		showEventText:  false,
        trackHeight:    0.4,
        trackGap:       0.1,
        width:          "25%", 
		eventSource:    eventSource,
        intervalUnit:   Timeline.DateTime.WEEK, 
        intervalPixels: 300
    })
  ];
  bandInfos[1].syncWith = 0;
  bandInfos[1].highlight = true;
  tl = Timeline.create(document.getElementById("my-timeline"), bandInfos);
  Timeline.loadXML("kyzek.xml", function(xml, url) { eventSource.loadXML(xml, url); });
}

var resizeTimerID = null;
function onResize() {
    if (resizeTimerID == null) {
        resizeTimerID = window.setTimeout(function() {
            resizeTimerID = null;
            tl.layout();
        }, 500);
    }
}

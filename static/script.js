const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
  const range = wrap.querySelector(".range");
  const bubble = wrap.querySelector(".bubble");

  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});

function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;

  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

var slide = document.getElementById('slide'),
    sliderDiv = document.getElementById("sliderAmount");

slide.onchange = function() {
    sliderDiv.innerHTML = this.value;
    $.post({
            url: '/',
            data: $('form').serialize(),
            success: function(response){
                alert(response);
                alert(response.volume);             // works with jsonify()
                alert(JSON.parse(response).volume); // works with json.dumps()
                console.log(response);
            },
            error: function(error){
                alert(response);
                console.log(error);
            }
        });
}
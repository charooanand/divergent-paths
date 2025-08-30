const scroller = scrollama();

  scroller
    .setup({
      step: "#scrolly-intro .step",
      offset: 0.5,
    })
    .onStepEnter(response => {
      console.log("Entered step:", response.index);
    });



    

const scrollerFade = scrollama();
scrollerFade
  .setup({
    step: "#scrolly-fade .step",
    offset: 0.5,
    debug: false,
  })
  .onStepEnter(response => {
    const step = response.element.dataset.step;
    let opacity;

    if (step === "1") {
      opacity = 0.2;
    } else if (step === "2") {
      opacity = 0.5;
    } else if (step === "3") {
      opacity = 1;
    } else {
      opacity = 1; // default
    }

    document.getElementById("fading-box").style.opacity = opacity;

  });



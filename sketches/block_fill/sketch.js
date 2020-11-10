let unit = 100;

function setup() {
    w = unit * 10;
    h = unit * 6;
    createCanvas(w, h);
    background('black');
}

function draw() {
    noFill();
    stroke(255);
    let unit = 100;

    timer = frameCount * 4;
    if(timer <= 255) {
        fill(timer);
    }
    rect(100, 100, unit, unit);

    timer = frameCount * 3;
    if(timer <= 255) {
        fill(timer);
    }
    rect(210, 100, unit, unit);

    timer = frameCount * 2;
    if(timer <= 255) {
        fill(timer);
    }
    rect(320, 100, unit, unit);

    timer = frameCount;
    if(timer <= 255) {
        fill(timer);
    }
    rect(430, 100, unit, unit);

    timer = frameCount / 2;
    if(timer <= 255) {
        fill(timer);
    }
    rect(540, 100, unit, unit);

    timer = frameCount / 4;
    if(timer <= 255) {
        fill(timer);
    }
    rect(650, 100, unit, unit);
}

// TODO: fill the 2nd minute
// TODO: figure out why fill breaks when units are 20
// TODO: expand to work for 3 minutes
// TODO: expand to work for 10, block will need to be smaller
const unit = 50;
const max_timer = 120;
// TODO: rename items
let timer = 59;
let animation_value = 0;

function setup() {
    w = unit * 10;
    // TODO: link to max timer
    h = unit * 12;
    createCanvas(w, h);
    background('black');
}

function draw() {
    noFill();
    stroke(255);
    console.log(frameCount);
    if (frameCount == 1) {
        draw_blocks(timer);
    }
    if (frameCount % 60 == 0) {
        timer++;
        if (timer <= max_timer) {
            draw_block(timer);
        }
    }

    // how can I skip the frameCount?
    // Could I use a combination of timer and frameCount?
    if (timer >= 60) {
        animation_value++;
        // TODO: cap at 255
        fill_cell(animation_value);
    }
}


function fill_cell(number) {
    console.log(number);
    // TODO: do I need to work with alpha or opacity here?
    // blendMode(MULTIPLY);
    fill(255, number / 180);
    //fill('rgb(100%,0%,10%)');
    blocks_per_row = 10
    y = 300; // unit size * blocks_per_column
    x = 0;
    rect(x, y, unit * blocks_per_row, unit * 6);
    noFill();
}

function draw_blocks(number) {
    for(n=1; n<=number; n++){
        draw_block(n);
    }
}

function draw_block(number) {
    // blocks are zero indexed
    number -= 1;
    // TODO: pass in as parameter
    blocks_per_row = 10

    row = int(number / blocks_per_row)
    y = height - unit - (row * unit);

    column = (number % blocks_per_row)
    x = column * unit;
    // console.log(row, column)
    rect(x, y, unit, unit);
}
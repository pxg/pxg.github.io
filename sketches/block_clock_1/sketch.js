let unit = 100;
let timer = 0;

function setup() {
    w = unit * 10;
    h = unit * 6;
    createCanvas(w, h);
    background('black');
}

function draw() {
    noFill();
    stroke(255);
    if (frameCount % 60 == 0) {
        timer++;
        // TODO: replae with max timer variable
        if (timer == 61){
            timer = 0;
            background('black');
        }else{
            draw_block(timer);
        }
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
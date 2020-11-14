var cols = 10
var rows = 10

function setup(){
    createCanvas(300,300)
}

function draw(){
    background(51)

    for(var i=0; i<cols; i++){
        for(var i=0; i<rows; i++){
            var x = i * 30
            var y = i * 30
            stroke(0)
            fill(255)
            rect (x, y, 30, 30)
        }
    }
}
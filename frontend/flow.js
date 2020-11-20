(function() {
    var _lastColor = null,
    _currentColor,

    _lastBlock = null,
    _currentBlock,

    _currentPath = {},

    _isTracing = false,

    _size,
    _moves = 0,

    _init = function() {

        levels = ['a1abc2bc', '2b7gfe5d10d1f3b1g2e1c2ca1h3a5h5', '4o1i9l6a11eb5g5e20j2g26n9f1f9l7h1o7n10j7c6pd3mc4h5p6im3kad23b2k1'];

        _loadLevel(levels[Math.floor(Math.random() * levels.length)]);

        var grid = document.querySelector('.grid');

        _size = parseInt(grid.getAttribute('data-size'));

        Array.from(grid.querySelectorAll('div')).forEach(function(block, i) {
            var colorId = parseInt(block.getAttribute('data-id')),
            isPoint = block.getAttribute('data-point') === 'true';

            block.setAttribute('data-i', i);
        });
    },
    _loadLevel = function(s) {
        var data = [];

        while (s.length) {
            s = s.replace(/^\d+|[a-z]/i, function(x) {
                if (parseInt(x)) {
                    while (x--) {
                        data.push(0);
                    }
                }
                else {
                    data.push(parseInt(x, 36) - 9);
                }

                return '';
            });
        }

        var grid = document.querySelector('.grid'),
        size = Math.sqrt(data.length);

        if (size !== parseInt(size)) {
            // throw 'Invalid grid definition.'; //
            console.error('Invalid grid definition.');

            return;
        }
        else {
            grid.setAttribute('data-size', size);
        }

        grid.innerHTML = '';

        data.forEach(function(n) {
            var block = document.createElement('div');

            if (n) {
                block.setAttribute('data-id', n);
                block.setAttribute('data-point', 'true');
            }

            grid.appendChild(block);
        });
    },
    _loadnew = function(){
        print("hello");
    };


    _init();
})();

# Doomed to Repeat It

This is a (golang + javascript) memory game.

## Vulnerability

```go
// OsRand gets some randomness from the OS.
func OsRand() (uint64, error) {
	// 64 ought to be enough for anybody
	var res uint64
	if err := binary.Read(rand.Reader, binary.LittleEndian, &res); err != nil {
		return 0, fmt.Errorf("couldn't read random uint64: %v", err)
	}
	// Mix in some of our own pre-generated randomness in case the OS runs low.
	// See Mining Your Ps and Qs for details.
	res *= 14496946463017271296
	fmt.Println("random", res);
	return res, nil
}
```

`hex(14496946463017271296) == 0xc92f800000000000` the lower bits of pre-generated randomness are zero. Only Ffwer seeds are generated, that can be bruteforced.

## Exploit


```go
func main() {
	a := [28][28][28][28][]int{}

	b := &board{
			nums:    make([]int, 56),
			visible: make([]bool, 56),
		}

	for loop := 0; loop < 0x100000; loop++ {
		// fmt.Println(i)
		if (loop % 0x1000 == 0) {
			fmt.Println("here", loop / 0x1000)
		}

		rand, _ := random.New2(uint64(loop))
		
		// BoardSize is even
		for i, _ := range b.nums {
			b.nums[i] = i / 2
		}
		// https://github.com/golang/go/wiki/SliceTricks#shuffling
		for i := 56 - 1; i > 0; i-- {
			j := rand.UInt64n(uint64(i) + 1)
			// fmt.Println(j);
			b.nums[i], b.nums[j] = b.nums[j], b.nums[i]
		}

		a[b.nums[0]][b.nums[1]][b.nums[2]][b.nums[3]] = append(a[b.nums[0]][b.nums[1]][b.nums[2]][b.nums[3]], loop)
	}

	file, _ := json.Marshal(a)
 
	_ = ioutil.WriteFile("test.json", file, 0644)
	...
```


```javascript
protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
ws = new WebSocket(protocol + window.location.host + '/ws');

let table = [];

ws.onopen = () => {
	ws.send(JSON.stringify({op: 'guess', body: {X: 0, Y: 0}}));
	ws.send(JSON.stringify({op: 'guess', body: {X: 1, Y: 0}}));
	ws.send(JSON.stringify({op: 'guess', body: {X: 2, Y: 0}}));
	ws.send(JSON.stringify({op: 'guess', body: {X: 3, Y: 0}}));
}
ws.onmessage = (x) => {
    let y = JSON.parse(x.data);
    let board = y.board;
	for (let i=0; i<board.length; i++) {
		if (board[i] != -1) table[i] = board[i]
    }
	console.log('Find..', table)
};

function submit(answer) {
	table = answer;
	console.log('pre', table);
	let i, j;
	for (i=0; i<answer.length; i++) {
		if (table[i] == -1) continue;
		for (j=i+1; j<answer.length; j++) {
			if (table[i] == table[j]) break;
        }
		console.log('answer!', i, j, table[i], table[j]);
		table[i] = table[j] = -1;
		ws.send(JSON.stringify({op: 'guess', body: {X: parseInt(i%7), Y: parseInt(i/7)}}));
		ws.send(JSON.stringify({op: 'guess', body: {X: parseInt(j%7), Y: parseInt(j/7)}}));
    }
}
```

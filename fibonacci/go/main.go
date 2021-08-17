package main
import "fmt"
import "time"

// sync:       6.889338ms
func fib_sync(n int) int {
    if (n < 2) {
        return n
	}
    return fib_sync(n - 1) + fib_sync(n - 2)
}

// async:      699.227863ms
func fib_async(n int) int {
    if (n < 2) {
        return n
	}
	out := make(chan int)
	go func() { out <- fib_async(n - 1) }()
    return <-out + fib_async(n - 2)
}

// full_async: 3.418636243s
// too many goroutines created
func fib_full_async(n int) int {
    if (n < 2) {
        return n
	}
	out1 := make(chan int)
	go func() { out1 <- fib_full_async(n - 1) }()
    out2 := make(chan int)
    go func() { out2 <- fib_full_async(n - 2) }()
    return <-out1 + <-out2
}

func main(){
    start := time.Now()
	fmt.Printf("%d\n", fib_sync(30))
    elapsed := time.Since(start)
    fmt.Printf("sync:       %s\n", elapsed)

    start = time.Now()
	fmt.Printf("%d\n", fib_async(30))
    elapsed = time.Since(start)
    fmt.Printf("async:      %s\n", elapsed)

    start = time.Now()
	fmt.Printf("%d\n", fib_full_async(30))
    elapsed = time.Since(start)
    fmt.Printf("full_async: %s\n", elapsed)
}

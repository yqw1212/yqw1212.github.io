package main

import (
	"encoding/hex"
	"fmt"
)

func GwSqNHQ7dPXpIG64(cJPTR string) string {
	YrXQd := hex.EncodeToString([]byte(cJPTR))
	return fmt.Sprintf("%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c", YrXQd[22], YrXQd[19], YrXQd[20], YrXQd[21], YrXQd[28], YrXQd[10], YrXQd[20], YrXQd[7], YrXQd[29], YrXQd[14], YrXQd[0], YrXQd[18], YrXQd[3], YrXQd[24], YrXQd[27], YrXQd[31])
}

func cHZv5op8rOmlAkb6(HIGXt []byte, VGvny string, ZOkKV string, eU0uD string) string {
	QTk4l := make([]byte, 20)
	Ek08m := [16]byte{
		167, 238, 45, 89, 160, 95, 34, 175, 158, 169, 20, 217, 68, 137, 231, 54}
	for i := 0; i < 16; i++ {
		QTk4l[i] += Ek08m[i] ^ HIGXt[i]
	}

	return string(QTk4l)
}

func JqZXm8BtAWL5cMEO() string {
	woaMV := []byte{
		159, 141, 72, 106, 196, 62, 16, 205, 170, 159, 36, 232, 125, 239, 208, 3}
	var ytUOA, b60Ph, meqHN string
	return cHZv5op8rOmlAkb6(woaMV, ytUOA, b60Ph, meqHN)
}

func main() {

	fmt.Printf("flag{%s%s}", GwSqNHQ7dPXpIG64("ZlXDJkH3OZN4Mayd"), JqZXm8BtAWL5cMEO())
}

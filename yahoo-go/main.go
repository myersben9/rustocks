package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"

	. "yahoo-stream/proto" // replace with your module path

	"github.com/gorilla/websocket"
	"google.golang.org/protobuf/proto"
)

func main() {
	conn, _, err := websocket.DefaultDialer.Dial("wss://streamer.finance.yahoo.com:443", nil)
	if err != nil {
		log.Fatal("Dial error:", err)
	}
	defer conn.Close()

	// Subscribe to symbols
	subMsg := map[string]interface{}{
		"subscribe": []string{
			"AAPL", // ... (same symbols as before)
		},
	}

	err = conn.WriteJSON(subMsg)
	if err != nil {
		log.Fatal("Write error:", err)
	}

	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			log.Println("Read error:", err)
			return
		}

		// Decode base64
		decoded, err := base64.StdEncoding.DecodeString(string(message))
		if err != nil {
			log.Println("Base64 decode error:", err)
			continue
		}

		// Unmarshal protobuf
		pricingData := &PricingData{}
		if err := proto.Unmarshal(decoded, pricingData); err != nil {
			log.Println("Protobuf unmarshal error:", err)
			continue
		}

		// Convert to JSON
		jsonData, err := json.MarshalIndent(pricingData, "", "  ")
		if err != nil {
			log.Println("JSON marshal error:", err)
			continue
		}

		fmt.Printf("Received update:\n%s\n\n", jsonData)
	}
}

// main.go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/aws/aws-lambda-go/lambda"
)

// Types
type Response struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

type ResponseBody struct {
	Timestamp string                 `json:"timestamp"`
	Symbol    string                 `json:"symbol"`
	Data      map[string]interface{} `json:"data"`
}

type Event struct {
	Time   string `json:"time"`
	Symbol string `json:"symbol"`
}

type Config struct {
	AlphaVantageKey string
	PolygonIOKey    string
	FinnhubKey      string
	FMPKey          string
	EODHDToken      string
}

// Client
type Client struct {
	httpClient *http.Client
}

func NewClient() *Client {
	return &Client{
		httpClient: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

func (c *Client) fetchData(url string) (map[string]interface{}, error) {
	resp, err := c.httpClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, err
	}

	return result, nil
}

// API Methods
func (c *Client) FetchAlphaVantage(symbol, apiKey string) map[string]interface{} {
	url := fmt.Sprintf("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s", symbol, apiKey)
	data, err := c.fetchData(url)
	if err != nil {
		log.Printf("AlphaVantage API error: %v", err)
		return nil
	}
	return data
}

func (c *Client) FetchPolygonIO(symbol, apiKey string) map[string]interface{} {
	url := fmt.Sprintf("https://api.polygon.io/v2/aggs/ticker/%s/prev?adjusted=true&apiKey=%s", symbol, apiKey)
	data, err := c.fetchData(url)
	if err != nil {
		log.Printf("Polygon.io API error: %v", err)
		return nil
	}
	return data
}

func (c *Client) FetchFinnhub(symbol, apiKey string) map[string]interface{} {
	url := fmt.Sprintf("https://finnhub.io/api/v1/quote?symbol=%s&token=%s", symbol, apiKey)
	data, err := c.fetchData(url)
	if err != nil {
		log.Printf("Finnhub API error: %v", err)
		return nil
	}
	return data
}

func (c *Client) FetchFMP(symbol, apiKey string) map[string]interface{} {
	url := fmt.Sprintf("https://financialmodelingprep.com/api/v3/quote/%s?apikey=%s", symbol, apiKey)
	data, err := c.fetchData(url)
	if err != nil {
		log.Printf("Financial Modeling Prep API error: %v", err)
		return nil
	}
	return data
}

func (c *Client) FetchEODHD(symbol, apiToken string) map[string]interface{} {
	url := fmt.Sprintf("https://eodhd.com/api/real-time/%s.US?api_token=%s&fmt=json", symbol, apiToken)
	data, err := c.fetchData(url)
	if err != nil {
		log.Printf("EOD Historical Data API error: %v", err)
		return nil
	}
	return data
}

// Configuration
func getConfig() Config {
	return Config{
		AlphaVantageKey: os.Getenv("ALPHAVANTAGE_API_KEY"),
		PolygonIOKey:    os.Getenv("POLYGONIO_API_KEY"),
		FinnhubKey:      os.Getenv("FINNHUB_API_KEY"),
		FMPKey:          os.Getenv("FMP_API_KEY"),
		EODHDToken:      os.Getenv("EODHD_API_TOKEN"),
	}
}

// Service
func fetchFinancialData(config Config, symbol string) map[string]interface{} {
	results := make(map[string]interface{})
	client := NewClient()
	var wg sync.WaitGroup
	var mu sync.Mutex

	// Helper function to safely store results
	storeResult := func(key string, data map[string]interface{}) {
		mu.Lock()
		results[key] = data
		mu.Unlock()
	}

	if config.AlphaVantageKey != "" {
		wg.Add(1)
		go func() {
			defer wg.Done()
			storeResult("alphavantage", client.FetchAlphaVantage(symbol, config.AlphaVantageKey))
		}()
	}

	if config.PolygonIOKey != "" {
		wg.Add(1)
		go func() {
			defer wg.Done()
			storeResult("polygonio", client.FetchPolygonIO(symbol, config.PolygonIOKey))
		}()
	}

	if config.FinnhubKey != "" {
		wg.Add(1)
		go func() {
			defer wg.Done()
			storeResult("finnhub", client.FetchFinnhub(symbol, config.FinnhubKey))
		}()
	}

	if config.FMPKey != "" {
		wg.Add(1)
		go func() {
			defer wg.Done()
			storeResult("fmp", client.FetchFMP(symbol, config.FMPKey))
		}()
	}

	if config.EODHDToken != "" {
		wg.Add(1)
		go func() {
			defer wg.Done()
			storeResult("eodhd", client.FetchEODHD(symbol, config.EODHDToken))
		}()
	}

	wg.Wait()
	return results
}

// Lambda Handler
func HandleRequest(event Event) (Response, error) {
	log.Printf("Starting financial data check at %v...", event.Time)
	
	if event.Symbol == "" {
		event.Symbol = "AAPL"
	}

	config := getConfig()
	results := fetchFinancialData(config, event.Symbol)

	responseBody := ResponseBody{
		Timestamp: time.Now().String(),
		Symbol:    event.Symbol,
		Data:      results,
	}

	bodyJSON, err := json.Marshal(responseBody)
	if err != nil {
		return Response{
			StatusCode: 500,
			Body:       fmt.Sprintf(`{"error": "%s", "timestamp": "%s"}`, err.Error(), time.Now().String()),
		}, err
	}

	return Response{
		StatusCode: 200,
		Body:       string(bodyJSON),
	}, nil
}

func main() {
	lambda.Start(HandleRequest)
}
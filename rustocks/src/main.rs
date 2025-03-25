use reqwest;
use scraper::{Html, Selector};
use tokio::time::{sleep, Duration};

async fn fetch_stock_price(symbol: &str) -> Result<String, reqwest::Error> {
    let url = format!("https://finance.yahoo.com/quote/{}", symbol);
    
    let client = reqwest::Client::new();
    let response = client.get(&url)
        .header(
            "User-Agent", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        )
        .send().await?
        .text().await?;
    
    let document = Html::parse_document(&response);
    let selector = Selector::parse(r#"span[data-testid="qsp-price"]"#).unwrap();

    if let Some(element) = document.select(&selector).next() {
        return Ok(element.text().collect::<String>());
    }

    Ok("Price not found".to_string())
}

#[tokio::main]
async fn main() {
    let stock_symbol = "AAPL";
    let mut previous_price = String::new();

    loop {
        match fetch_stock_price(stock_symbol).await {
            Ok(price) => {
                if price != previous_price {
                    println!("{} price: {}", stock_symbol, price);
                    previous_price = price;
                }
            },
            Err(err) => eprintln!("Error fetching stock price: {}", err),
        }
        sleep(Duration::from_secs(1)).await;
    }
}

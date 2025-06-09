# 🔍 Enhanced Scrapy-AI-Contact-Finder

A comprehensive AI-powered contact finder that searches multiple online sources to find contact information for companies worldwide. Features advanced AI research, batch processing, and comprehensive data export capabilities.

## ✨ Key Features

### 🚀 **New Enhancements**
- **Persistent Model Selection**: AI model selection now persists and doesn't change automatically
- **Comprehensive Model Library**: Access to 100+ OpenRouter models including free and paid options
- **Multi-Source Contact Discovery**: Searches websites, LinkedIn, business directories, WHOIS, and more
- **Batch CSV Processing**: Process hundreds of companies at once
- **Advanced Export Options**: Export to CSV and Excel with multiple sheets
- **Real-time Progress Tracking**: Monitor batch processing progress
- **Enhanced Error Handling**: Better retry mechanisms and error reporting

### 🎯 **Search Capabilities**
- **AI-Powered Research**: Uses advanced language models with web search capabilities
- **Website Deep Crawl**: Extracts contacts from company websites, including hidden pages
- **Professional Networks**: Searches LinkedIn, Xing (German), and other professional platforms
- **Business Directories**: Mines Google Business, Yellow Pages, Chamber of Commerce listings
- **WHOIS Domain Data**: Extracts registration and technical contact information
- **News & Press Coverage**: Finds executives mentioned in recent articles
- **Government Sources**: Searches corporate registrations and legal filings

### 📊 **Data Sources**
1. **Official Websites**: Contact pages, about sections, team directories
2. **LinkedIn & Xing**: Professional profiles and company pages
3. **Business Directories**: Local and industry-specific listings
4. **Press & Media**: News articles, press releases, interviews
5. **Technical Sources**: WHOIS, DNS records, SSL certificates
6. **Social Media**: Facebook, Twitter, YouTube channel information
7. **Legal Sources**: Corporate registrations, SEC filings, patents

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/scrapy-ai-contact-finder.git
cd scrapy-ai-contact-finder
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the project root:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

4. **Get OpenRouter API Key**:
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Sign up for an account
   - Generate an API key
   - Add credits to your account (some models are free)

## 🚀 Usage

### **Single Company Search**

1. **Run the application**:
```bash
streamlit run scrapy_email_finder.py
```

2. **Configure settings**:
   - Select AI model category (Web Search recommended)
   - Choose specific model
   - Enable search methods

3. **Enter company details**:
   - Company name
   - Website URL
   - Country
   - Industry (optional)

4. **Start search** and review comprehensive results

### **Batch CSV Processing**

1. **Download CSV template** from the app
2. **Fill in company information**:
   ```csv
   company,website,country,industry
   Example Corp,example.com,Germany,Technology
   Another Company,anothercompany.com,USA,Manufacturing
   ```
3. **Upload CSV file** and click "Process All Companies"
4. **Download combined results** in CSV or Excel format

## 📋 CSV Template Format

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| company | Yes | Official company name | BBW Berufsbildungswerk Hamburg |
| website | Yes | Company website URL | bbw.de |
| country | Yes | Company location | Germany |
| industry | No | Industry sector | Education |

## 🤖 AI Model Categories

### **Web Search Models (Recommended)**
- **Perplexity Sonar**: Real-time web search capabilities
- **Other Online Models**: Various models with internet access
- **Best for**: Current information, recent changes, comprehensive research

### **Free Models**
- **Limited Credits**: Some models offer free usage
- **Basic Capabilities**: Text processing without web search
- **Best for**: Pattern recognition, email format guessing

### **Premium Models**
- **Advanced AI**: GPT-4, Claude, and other premium models
- **Higher Accuracy**: Better understanding and reasoning
- **Best for**: Complex analysis, high-value searches

## 📊 Output Formats

### **Structured Data Table**
| Name | Role/Title | LinkedIn/Profile URL | Email | Phone | Source | Confidence | Notes |
|------|------------|---------------------|--------|-------|--------|------------|-------|
| Dr. Hans Mueller | CEO | https://linkedin.com/in/hansmueller | h.mueller@domain.com | +49-40-123456 | LinkedIn + Website | High | 15 years experience |

### **Export Options**
- **CSV**: Simple comma-separated format
- **Excel**: Multi-sheet workbook with:
  - All Contacts sheet
  - Summary sheet with processing statistics
  - Formatted data with hyperlinks

## 🌍 Country-Specific Features

### **Germany**
- **Impressum Page**: Legally required contact information
- **Xing Integration**: German professional network
- **Business Registration**: Bundesanzeiger and local registers
- **German Titles**: Geschäftsführer, Bereichsleiter, etc.

### **United States**
- **SEC Filings**: Public company executive information
- **Better Business Bureau**: Business directory listings
- **LinkedIn Focus**: Primary professional network
- **State Registrations**: Corporate filing searches

### **Other Countries**
- **Local Directories**: Country-specific business listings
- **Professional Networks**: Regional LinkedIn equivalents
- **Legal Requirements**: Local contact disclosure laws

## ⚙️ Advanced Configuration

### **Search Method Combinations**
- **AI Research + WHOIS**: Comprehensive online + technical data
- **All Methods**: Maximum coverage (recommended for important searches)
- **AI Only**: Fast, comprehensive research without technical lookup

### **Rate Limiting & Performance**
- **Batch Processing**: Automatic delays between requests
- **Error Handling**: Retry mechanisms for failed requests
- **Progress Tracking**: Real-time status updates
- **Resource Management**: Efficient API usage

## 🛡️ Privacy & Ethics

### **Data Handling**
- **No Storage**: Contact data is not stored on servers
- **Local Processing**: All data processing happens in your browser
- **Export Control**: You control where data is saved
- **API Security**: Secure communication with AI providers

### **Ethical Use**
- **Public Information**: Only searches publicly available data
- **Respect Robots.txt**: Follows website crawling guidelines
- **No Harassment**: Intended for legitimate business communication
- **GDPR Compliance**: Respects European privacy regulations

## 🔧 Troubleshooting

### **Common Issues**

1. **No Results Found**:
   - Verify website URL is correct and accessible
   - Try alternative company name spellings
   - Check if company has public contact information
   - Use Web Search models for better coverage

2. **API Errors**:
   - Check OpenRouter API key is valid
   - Verify account has sufficient credits
   - Try different model if current one fails
   - Check network connectivity

3. **Slow Performance**:
   - Use faster models for batch processing
   - Process smaller batches (10-50 companies)
   - Check internet connection speed
   - Consider upgrading to premium models

4. **CSV Upload Issues**:
   - Ensure CSV has required columns: company, website, country
   - Check for special characters in company names
   - Verify website URLs are properly formatted
   - Use UTF-8 encoding for international characters

### **Performance Tips**

1. **Model Selection**:
   - Use Web Search models for best results
   - Choose faster models for large batches
   - Premium models offer higher accuracy

2. **Batch Processing**:
   - Process during off-peak hours
   - Start with small test batches
   - Monitor API usage and costs
   - Save results frequently

3. **Search Optimization**:
   - Include industry information when possible
   - Use official company names with legal entities
   - Verify website accessibility before processing
   - Check for recent company changes or mergers

## 🆘 Support

### **Getting Help**
1. **Check this README** for common solutions
2. **Review error messages** for specific guidance
3. **Test with single company** before batch processing
4. **Verify API key and credits** in OpenRouter dashboard

### **Reporting Issues**
- Provide error messages and steps to reproduce
- Include company information (if not sensitive)
- Specify which AI model was used
- Share browser console errors if applicable

## 📈 Future Enhancements

- **CRM Integration**: Direct export to Salesforce, HubSpot
- **Email Verification**: Validate email addresses in real-time
- **Social Media Expansion**: Instagram, TikTok business profiles
- **API Endpoint**: Direct API access for developers
- **Chrome Extension**: Browser-based contact finding
- **Data Enrichment**: Company size, revenue, funding information

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ for business development and sales professionals worldwide**

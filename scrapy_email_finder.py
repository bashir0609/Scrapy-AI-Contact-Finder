import streamlit as st
import requests
import pandas as pd
import re
from datetime import datetime
import validators
import whois
from urllib.parse import urlparse
import time

def create_enhanced_search_prompt(company, website, country, industry=""):
    """Enhanced prompt that searches multiple sources"""
    domain = website.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
    
    prompt = f"""
You are a professional business research assistant with real-time web browsing capabilities.

**PRIMARY TASK**: Find current contact information for executives and key personnel at {company} (website: {website}), located in {country}.

**MULTI-SOURCE SEARCH STRATEGY**:

1. **Company Website Deep Search**:
   - Check {website}/contact, {website}/about, {website}/team, {website}/impressum (for German sites)
   - Look for leadership pages, staff directories, office locations

2. **LinkedIn Professional Network**:
   - Search for current employees at "{company}"
   - Focus on: C-level executives, Directors, Department Heads, HR managers
   - Get LinkedIn profile URLs when possible

3. **Business Directories & Databases**:
   - Search business registries, chamber of commerce listings
   - Look for Xing profiles (popular in Germany)
   - Check industry-specific directories

4. **Press Releases & News**:
   - Recent articles mentioning company executives
   - Press releases with spokesperson contacts
   - Industry publications and interviews

5. **Domain Registration (WHOIS)**:
   - Check domain registration details for admin contacts
   - Look for technical and billing contact information

**OUTPUT REQUIREMENTS**:

Return a markdown table with these columns:
| Name | Role | LinkedIn/Xing URL | Email | Source | Confidence |

**Email Guidelines**:
- Use confirmed emails when found
- For educated guesses based on patterns, mark as "(estimated)"
- Include general company emails (info@, contact@, office@)
- For German companies, check for impressum emails

**Confidence Levels**:
- High: Confirmed from official sources
- Medium: Found in reliable business directories  
- Low: Educated guess based on patterns

**Example Output**:
| Name | Role | LinkedIn/Xing URL | Email | Source | Confidence |
|------|------|-------------------|--------|--------|--------|------------|
| Hans Mueller | CEO | https://www.linkedin.com/in/hansmueller | h.mueller@{domain} | LinkedIn + Company Website | High |
| Sarah Schmidt | HR Director | https://www.xing.com/profile/SarahSchmidt | info@{domain} | | Company Website | Medium |
| | General Contact | | contact@{domain} | +49... | Website Contact Page | High |

**Important for German Companies**:
- Check "Impressum" page (legally required contact info)
- Look for Xing profiles (German LinkedIn equivalent)
- Search for GmbH/AG registration details
- Include proper German business titles (Geschäftsführer, etc.)

**Sources Section**:
After the table, list all sources with clickable links:
- [Source Name](URL)

If you cannot find sufficient current information, explain your search process and suggest alternative research approaches.

Begin comprehensive research for {company} now.
"""
    
    return prompt

def query_openrouter_enhanced(api_key, model, prompt):
    """Enhanced API query with better error handling"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 3000  # Increased for more comprehensive results
    }
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=90)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                wait_time = (attempt + 1) * 10
                st.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                st.error(f"API error {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            st.warning(f"Request timeout on attempt {attempt + 1}/3")
            if attempt < 2:
                time.sleep(5)
        except Exception as e:
            if attempt == 2:
                raise Exception(f"Failed after 3 attempts: {str(e)}")
            time.sleep(5)
    
    return None

def get_whois_contacts(domain):
    """Extract contacts from WHOIS data"""
    try:
        w = whois.whois(domain)
        contacts = {
            'registrar_email': None,
            'admin_email': None,
            'tech_email': None,
            'org_name': None
        }
        
        if hasattr(w, 'emails') and w.emails:
            if isinstance(w.emails, list):
                contacts['registrar_email'] = w.emails[0] if w.emails else None
            else:
                contacts['registrar_email'] = w.emails
        
        if hasattr(w, 'org') and w.org:
            contacts['org_name'] = w.org
            
        return contacts
    except Exception as e:
        st.warning(f"WHOIS lookup failed: {e}")
        return None

def main():
    st.set_page_config(
        page_title="Scrapy + AI Contact Finder",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Multi-Source Scrapy + AI Contact Finder")
    st.markdown("*AI research + Website crawling + WHOIS lookup + Professional networks*")
    
    # Load API key
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        api_key = st.text_input("🔐 OpenRouter API Key", type="password")
        if not api_key:
            st.error("API key required")
            st.stop()
    
    # Get models
    try:
        resp = requests.get("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {api_key}"})
        models = resp.json()["data"]
        model_list = [model["id"] for model in models if "perplexity" in model["id"] or "online" in model["id"]]
        preferred_model = "perplexity/llama-3-sonar-large-online"
        default_model = preferred_model if preferred_model in model_list else model_list[0]
    except:
        st.error("Failed to load models")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Search Settings")
        
        model = st.selectbox("AI Model", model_list, index=model_list.index(default_model))
        
        search_methods = st.multiselect(
            "Search Methods",
            ["AI Research", "WHOIS Lookup", "Website Crawling"],
            default=["AI Research", "WHOIS Lookup"]
        )
        
        st.markdown("---")
        st.caption("🎯 **Recommended**: Start with AI Research for best results")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.text_input("🏢 Company Name", placeholder="e.g., BBW Berufsbildungswerk")
        website = st.text_input("🌐 Website", placeholder="e.g., bbw.de")
    
    with col2:
        country = st.text_input("📍 Country", value="Germany")
        industry = st.text_input("🏭 Industry (Optional)", placeholder="e.g., Education, Technology")
    
    # Search button
    if st.button("🚀 Multi-Source Search", type="primary"):
        if not all([company, website, country]):
            st.error("Please fill in company, website, and country")
            return
        
        # Validate website
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        if not validators.url(website):
            st.error("Invalid website URL")
            return
        
        domain = urlparse(website).netloc.replace('www.', '')
        
        # Results container
        results_container = st.container()
        
        with results_container:
            # Method 1: WHOIS Lookup (fast)
            if "WHOIS Lookup" in search_methods:
                with st.expander("📋 WHOIS Domain Information", expanded=True):
                    with st.spinner("Looking up domain registration..."):
                        whois_data = get_whois_contacts(domain)
                        
                        if whois_data:
                            col1, col2 = st.columns(2)
                            with col1:
                                if whois_data['org_name']:
                                    st.info(f"**Registered Organization**: {whois_data['org_name']}")
                                if whois_data['registrar_email']:
                                    st.info(f"**Registrar Email**: {whois_data['registrar_email']}")
                            with col2:
                                if whois_data['admin_email']:
                                    st.info(f"**Admin Email**: {whois_data['admin_email']}")
                                if whois_data['tech_email']:
                                    st.info(f"**Technical Email**: {whois_data['tech_email']}")
                        else:
                            st.warning("No WHOIS contact information available")
            
            # Method 2: AI Research (most comprehensive)
            if "AI Research" in search_methods:
                st.subheader("🧠 AI-Powered Research Results")
                
                with st.spinner("🔍 Conducting comprehensive research across multiple sources..."):
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Create enhanced prompt
                    status_text.text("📝 Preparing comprehensive search strategy...")
                    progress_bar.progress(20)
                    
                    prompt = create_enhanced_search_prompt(company, website, country, industry)
                    
                    # Execute AI search
                    status_text.text("🌐 Searching LinkedIn, business directories, and web sources...")
                    progress_bar.progress(60)
                    
                    result = query_openrouter_enhanced(api_key, model, prompt)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Research completed!")
                    
                    if result:
                        # Display results
                        with st.expander("📄 Full Research Report", expanded=True):
                            st.markdown(result)
                        
                        # Try to parse table
                        lines = result.split("\n")
                        table_lines = [line for line in lines if "|" in line and "---" not in line]
                        
                        if len(table_lines) >= 2:
                            try:
                                headers = [cell.strip() for cell in table_lines[0].split("|") if cell.strip()]
                                rows = []
                                for line in table_lines[1:]:
                                    cells = [cell.strip() for cell in line.split("|") if cell.strip()]
                                    if len(cells) >= 3:  # Minimum viable row
                                        while len(cells) < len(headers):
                                            cells.append("")
                                        rows.append(cells[:len(headers)])
                                
                                if rows:
                                    df = pd.DataFrame(rows, columns=headers)
                                    st.subheader("📊 Structured Contact Data")
                                    st.dataframe(df, use_container_width=True)
                                    
                                    # Export
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                                    csv_data = df.to_csv(index=False).encode("utf-8")
                                    st.download_button(
                                        "⬇️ Download Contact Data",
                                        data=csv_data,
                                        file_name=f"{company.lower().replace(' ', '_')}_contacts_{timestamp}.csv",
                                        mime="text/csv"
                                    )
                            except Exception as e:
                                st.info("Could not parse table format, but full results are shown above")
                        
                        # Extract citations
                        citations = re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", result)
                        if citations:
                            st.subheader("📚 Research Sources")
                            for i, (name, url) in enumerate(citations, 1):
                                st.markdown(f"{i}. [{name}]({url})")
                    else:
                        st.error("AI research failed. Please try again.")
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
    
    # Tips section
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **For German Companies:**
        - Check the "Impressum" page (legally required contact information)
        - Search Xing.com in addition to LinkedIn
        - Look for GmbH/AG company registration details
        
        **For Better AI Results:**
        - Use official company names (e.g., "BBW Berufsbildungswerk Hamburg GmbH")
        - Specify the industry to help focus the search
        - Try variations of the company name if no results
        
        **If No Results:**
        - Company might not have public contact information
        - Try calling their main number for contact details
        - Check industry associations or trade organizations
        - Look for the company on professional networks manually
        """)

if __name__ == "__main__":
    main()

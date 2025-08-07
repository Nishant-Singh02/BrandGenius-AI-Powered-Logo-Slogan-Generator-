document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    const logoGrid = document.getElementById('logo-grid');
    const sloganGrid = document.getElementById('slogan-grid');
    const regenerateBtn = document.getElementById('regenerate');
    const downloadAllBtn = document.getElementById('download-all');
    
    let currentLogos = [];
    let currentSlogans = [];
    
    generateBtn.addEventListener('click', generateBranding);
    regenerateBtn.addEventListener('click', generateBranding);
    downloadAllBtn.addEventListener('click', downloadAll);
    
    async function generateBranding() {
        const prompt = promptInput.value.trim();
        const selectedStyle = document.querySelector('.style-select').value; // <-- Get style

        if (!prompt) {
            alert('Please describe your brand to generate logos and slogans');
            return;
        }

        // Show loading state
        generateBtn.disabled = true;
        regenerateBtn.disabled = true;
        loadingSection.style.display = 'flex';
        resultsSection.style.display = 'none';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt, style: selectedStyle }) // <-- Send style to backend
            });

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            const data = await response.json();
            currentLogos = data.logos;
            currentSlogans = data.slogans;

            displayResults(data.logos, data.slogans);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during generation. Please try again.');
        } finally {
            loadingSection.style.display = 'none';
            generateBtn.disabled = false;
            regenerateBtn.disabled = false;
        }
    }

    
    function displayResults(logos, slogans) {
        // Clear previous results
        logoGrid.innerHTML = '';
        sloganGrid.innerHTML = '';
        
        // Display logos
        logos.forEach((logo, index) => {
            const logoItem = document.createElement('div');
            logoItem.className = 'logo-item';
            
            logoItem.innerHTML = `
                <img src="data:image/png;base64,${logo}" alt="Generated Logo ${index + 1}" class="logo-img">
                <div class="logo-actions">
                    <span>Logo ${index + 1}</span>
                    <button class="btn-secondary download-logo" data-index="${index}">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            `;
            
            logoGrid.appendChild(logoItem);
        });
        
        // Display slogans
        slogans.forEach((slogan, index) => {
            const sloganItem = document.createElement('div');
            sloganItem.className = 'slogan-item';
            
            sloganItem.innerHTML = `
                <p class="slogan-text">${slogan}</p>
                <div class="slogan-actions">
                    <button class="btn-secondary copy-slogan" data-slogan="${slogan}">
                        <i class="fas fa-copy"></i> Copy
                    </button>
                </div>
            `;
            
            sloganGrid.appendChild(sloganItem);
        });
        
        // Add event listeners for new buttons
        document.querySelectorAll('.download-logo').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = this.getAttribute('data-index');
                downloadLogo(logos[index], `logo-${index + 1}.png`);
            });
        });
        
        document.querySelectorAll('.copy-slogan').forEach(btn => {
            btn.addEventListener('click', function() {
                const slogan = this.getAttribute('data-slogan');
                navigator.clipboard.writeText(slogan);
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i> Copy';
                }, 2000);
            });
        });
        
        // Show results
        resultsSection.style.display = 'block';
    }
    
    function downloadLogo(logoData, filename) {
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${logoData}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    function downloadAll() {
        currentLogos.forEach((logo, index) => {
            setTimeout(() => {
                downloadLogo(logo, `logo-${index + 1}.png`);
            }, index * 300);
        });
        
        // Create a text file with slogans
        const slogansText = currentSlogans.map((slogan, i) => `Slogan ${i + 1}: ${slogan}`).join('\n\n');
        const blob = new Blob([slogansText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'slogans.txt';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
});
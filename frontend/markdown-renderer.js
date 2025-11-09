class MarkdownRenderer {
  static render(content) {
    const div = document.createElement('div');
    div.className = 'markdown-content';
    
    let html = content;
    
    // Process tables first (before other formatting)
    html = this.processTables(html);
    
    // Headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Bold and italic
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Code blocks
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
    
    // Lists with emojis
    html = html.replace(/^[-*] (.+)$/gm, '<li>$1</li>');
    html = html.replace(/^[✨🏗️☁️🔄📊🎨📐📝🧱📱💾⚡🔒✅🌐] \*\*(.+?)\*\*: (.+)$/gm, '<li><strong>$1</strong>: $2</li>');
    
    // Wrap consecutive li elements in ul
    html = html.replace(/((<li>.*?<\/li>\s*)+)/g, '<ul>$1</ul>');
    
    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';
    
    // Clean up
    html = html.replace(/<p>\s*<\/p>/g, '');
    html = html.replace(/<p>\s*(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<ul>)/g, '$1');
    html = html.replace(/(<\/ul>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<pre>)/g, '$1');
    html = html.replace(/(<\/pre>)\s*<\/p>/g, '$1');
    html = html.replace(/<p>\s*(<table>)/g, '$1');
    html = html.replace(/(<\/table>)\s*<\/p>/g, '$1');
    
    div.innerHTML = html;
    return div;
  }
  
  static processTables(content) {
    // Match markdown tables
    const tableRegex = /(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)*)/g;
    
    return content.replace(tableRegex, (match) => {
      const lines = match.trim().split('\n');
      if (lines.length < 2) return match;
      
      const headerLine = lines[0];
      const separatorLine = lines[1];
      const dataLines = lines.slice(2);
      
      // Parse header
      const headers = headerLine.split('|').map(h => h.trim()).filter(h => h);
      
      // Parse alignment from separator
      const alignments = separatorLine.split('|').map(s => {
        s = s.trim();
        if (s.startsWith(':') && s.endsWith(':')) return 'center';
        if (s.endsWith(':')) return 'right';
        return 'left';
      }).filter((_, i) => i < headers.length);
      
      // Build table HTML
      let tableHtml = '<table class="markdown-table">\n';
      
      // Header row
      tableHtml += '<thead><tr>';
      headers.forEach((header, i) => {
        const align = alignments[i] || 'left';
        tableHtml += `<th style="text-align: ${align}; font-weight: bold;">${this.processInlineFormatting(header)}</th>`;
      });
      tableHtml += '</tr></thead>\n';
      
      // Data rows
      if (dataLines.length > 0) {
        tableHtml += '<tbody>';
        dataLines.forEach(line => {
          if (line.trim()) {
            const cells = line.split('|').map(c => c.trim()).filter(c => c);
            tableHtml += '<tr>';
            cells.forEach((cell, i) => {
              const align = alignments[i] || 'left';
              tableHtml += `<td style="text-align: ${align};">${this.processInlineFormatting(cell)}</td>`;
            });
            tableHtml += '</tr>';
          }
        });
        tableHtml += '</tbody>';
      }
      
      tableHtml += '</table>';
      return tableHtml;
    });
  }
  
  static processInlineFormatting(text) {
    // Process bold, italic, and code within table cells
    let result = text;
    result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    result = result.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    result = result.replace(/`([^`]+)`/g, '<code>$1</code>');
    return result;
  }
}

// Enhanced CSS for tables
const tableStyles = `
.markdown-table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5em 0;
  font-family: 'Poppins', sans-serif;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.markdown-table th {
  background: linear-gradient(135deg, #232f3e, #39465a);
  color: white;
  font-weight: 700;
  padding: 12px 16px;
  text-align: left;
  border: none;
  font-size: 14px;
  letter-spacing: 0.5px;
}

.markdown-table td {
  padding: 10px 16px;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  font-size: 14px;
}

.markdown-table tbody tr:nth-child(even) td {
  background: #f8fafc;
}

.markdown-table tbody tr:hover td {
  background: #f1f5f9;
}

.markdown-table td strong {
  color: #1f2937;
  font-weight: 600;
}

.markdown-table td code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #374151;
}
`;

// Inject styles
if (!document.getElementById('markdown-table-styles')) {
  const style = document.createElement('style');
  style.id = 'markdown-table-styles';
  style.textContent = tableStyles;
  document.head.appendChild(style);
}
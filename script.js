let stockData = [];

async function queryStock() {
    const stockCode = document.getElementById('stockCode').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!stockCode || !startDate || !endDate) {
        alert('请填写完整的查询信息');
        return;
    }

    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                api_name: 'daily',
                params: {
                    ts_code: stockCode,
                    start_date: startDate.replace(/-/g, ''),
                    end_date: endDate.replace(/-/g, '')
                }
            })
        });

        const data = await response.json();
        if (data.data && data.data.items) {
            stockData = processStockData(data.data.items);
            renderTable(stockData);
        }
    } catch (error) {
        console.error('数据获取失败:', error);
        alert('数据获取失败，请稍后重试');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function processStockData(data) {
    // 计算移动平均线
    return data.map((item, index, array) => {
        const calculateMA = (days) => {
            if (index < days - 1) return null;
            const sum = array.slice(index - days + 1, index + 1)
                .reduce((acc, curr) => acc + curr[4], 0);
            return (sum / days).toFixed(2);
        };

        const priceRange = item[3] - item[4]; // 最高价 - 最低价
        const changePercent = ((item[2] - array[index + 1]?.[2]) / array[index + 1]?.[2] * 100).toFixed(2);

        return {
            date: item[1],
            open: item[2],
            close: item[3],
            high: item[4],
            low: item[5],
            priceRange: priceRange.toFixed(2),
            volume: item[6],
            ma3: calculateMA(3),
            ma5: calculateMA(5),
            ma10: calculateMA(10),
            ma20: calculateMA(20),
            ma50: calculateMA(50),
            ma120: calculateMA(120),
            volumeRatio: calculateVolumeRatio(item[6], array, index),
            turnoverRate: item[7],
            changePercent: changePercent
        };
    });
}

function calculateVolumeRatio(currentVolume, data, index) {
    if (index < 5) return null;
    const avgVolume = data.slice(index - 5, index)
        .reduce((acc, curr) => acc + curr[6], 0) / 5;
    return (currentVolume / avgVolume).toFixed(2);
}

function renderTable(data) {
    const tbody = document.getElementById('stockData');
    tbody.innerHTML = '';

    data.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.date}</td>
            <td>${item.open}</td>
            <td>${item.close}</td>
            <td>${item.high}</td>
            <td>${item.low}</td>
            <td>${item.priceRange}</td>
            <td>${item.ma3 || '-'}</td>
            <td>${item.ma5 || '-'}</td>
            <td>${item.ma10 || '-'}</td>
            <td>${item.ma20 || '-'}</td>
            <td>${item.ma50 || '-'}</td>
            <td>${item.ma120 || '-'}</td>
            <td>${item.volume}</td>
            <td>${item.volumeRatio || '-'}</td>
            <td>${item.turnoverRate}</td>
            <td class="${item.changePercent > 0 ? 'positive' : 'negative'}">${item.changePercent}%</td>
        `;
        tbody.appendChild(tr);
    });
}

// 初始化日期选择器
document.addEventListener('DOMContentLoaded', () => {
    const today = new Date();
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    
    document.getElementById('endDate').value = today.toISOString().split('T')[0];
    document.getElementById('startDate').value = lastMonth.toISOString().split('T')[0];
});

// 添加表格排序功能
document.querySelectorAll('th').forEach((header, index) => {
    header.addEventListener('click', () => {
        sortTable(index);
    });
});

function sortTable(column) {
    const tbody = document.getElementById('stockData');
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[column].textContent;
        const bValue = b.cells[column].textContent;
        return aValue.localeCompare(bValue, undefined, {numeric: true});
    });
    
    rows.forEach(row => tbody.appendChild(row));
} 
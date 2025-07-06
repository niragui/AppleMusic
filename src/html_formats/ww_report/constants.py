CSS_CONSTANTS = """
<head>
  <meta charset="UTF-8">
  <title>Country Ranking Card</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: #f4f4f4;
      padding: 20px;
    }

    .ranking-card {
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      max-width: 400px;
      margin: 0 auto;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .card-header, .card-footer {
      background-color: #FA2D48;
      color: #fff;
      padding: 15px 20px;
    }

    .card-header {
      display: flex;
      align-items: center;
    }

    .card-header img {
      width: 40px;
      height: 40px;
      margin-right: 15px;
    }

    .header-text {
      display: flex;
      flex-direction: column;
    }

    .header-text h2 {
      font-size: 1.2em;
      margin: 0;
    }

    .header-text .subtitle {
      font-size: 0.9em;
      color: #d0e6f7;
    }

    .country-item {
      display: flex;
      align-items: center;
      border-bottom: 1px solid #eee;
      padding: 12px 20px;
    }

    .country-item:last-child {
      border-bottom: none;
    }

    .flag {
      width: 40px;
      height: 25px;
      object-fit: cover;
      margin-right: 15px;
      border: 1px solid #ccc;
    }

    .country-info {
      flex: 1;
      font-weight: 500;
    }

    .position {
      font-weight: bold;
      font-size: 1.1em;
      color: #333;
    }

    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.9em;
    }

    .card-footer img {
      width: 20px;
      height: 20px;
      margin-right: 8px;
    }

    .bookmark {
      display: flex;
      align-items: center;
    }

    .date {
      font-style: italic;
    }
  </style>
</head>
"""
import { useEffect, useState } from "react";
import { getArticles } from "../services/api";

export default function ArticlesTable({ ticker }) {
  const [articles, setArticles] = useState(null);

  useEffect(() => {
    async function fetchArticles() {
      const articles = await getArticles(ticker);
      setArticles(articles);
    }

    fetchArticles();
  }, [ticker]);

  if (articles == null) return <h3>Fetching ...</h3>;

  return (
    <div class="table-card">
      <h2>Recent Articles</h2>
      <table>
        <thead>
          <tr>
            <th>TimeStamp</th>
            <th>Title / URL</th>
            <th>Sentiment</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {articles.map(article => (
            <tr key={article.id}>
              <td>{article.date_time}</td>
              <td>
                <a
                  href={article.link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {article.title}
                </a>
              </td>
              <td style={{ color: article.colour }}>{article.sa_label.toUpperCase()}</td>
              <td style={{ color: article.colour }}>{article.sa_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
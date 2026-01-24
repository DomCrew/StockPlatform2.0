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
    <div>
      <table>
        <thead>
          <tr>
            <th>TimeStamp</th>
            <th>Title</th>
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
              <td>{article.sa_label}</td>
              <td style={{ color: article.colour }}><strong>{article.sa_score}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
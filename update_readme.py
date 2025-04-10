import feedparser, time

URL = "https://chaesunbak.tistory.com/rss"
RSS_FEED = feedparser.parse(URL)
MAX_POST = 5
README_FILE = "README.md"

START_MARKER = "<!-- LATEST-BLOG-POST-LIST:START -->"
END_MARKER = "<!-- LATEST-BLOG-POST-LIST:END -->"

def update_readme_with_blog_posts():
    """README.md 파일에서 최신 블로그 포스트 목록을 업데이트합니다."""
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_content = f.readlines()
    except FileNotFoundError:
        print(f"Error: {README_FILE} 파일을 찾을 수 없습니다.")
        return

    start_marker_index = -1
    end_marker_index = -1

    for i, line in enumerate(readme_content):
        if START_MARKER in line:
            start_marker_index = i
        elif END_MARKER in line:
            end_marker_index = i
            break

    if start_marker_index == -1 or end_marker_index == -1 or start_marker_index >= end_marker_index:
        print("Error: README.md 파일에서 올바른 주석 마커를 찾을 수 없습니다.")
        return

    blog_posts_markdown = "### 최근 블로그 포스팅\n"
    for idx, feed in enumerate(RSS_FEED['entries']):
        if idx >= MAX_POST:
            break
        else:
            feed_date = feed['published_parsed']
            formatted_date = time.strftime('%Y/%m/%d', feed_date) if feed_date else "날짜 정보 없음"
            markdown_text = f"[{formatted_date} - {feed['title']}]({feed['link']}) <br/>\n"
            blog_posts_markdown += markdown_text

    updated_readme_content = (
        readme_content[: start_marker_index + 1]
        + [blog_posts_markdown]
        + readme_content[end_marker_index :]
    )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(updated_readme_content)
    print("README.md 파일이 최신 블로그 포스트로 업데이트되었습니다.")

if __name__ == "__main__":
    update_readme_with_blog_posts()

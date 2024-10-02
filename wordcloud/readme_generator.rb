# require_relative "./cloud_types"

class ReadmeGenerator
  WORD_CLOUD_URL = 'wordcloud/wordcloud.png'
  ADDWORD = 'add'
  SHUFFLECLOUD = 'shuffle'
  INITIAL_COUNT = 0
  USER = "t1noo7"

  def initialize(octokit:)
    @octokit = octokit
  end

  def generate
    participants = Hash.new(0)
    current_contributors = Hash.new(0)
    current_words_added = INITIAL_COUNT
    total_clouds = CloudTypes::CLOUDLABELS.length
    total_words_added = INITIAL_COUNT * total_clouds

    octokit.issues.each do |issue|
      participants[issue.user.login] += 1
      if issue.title.split('|')[1] != SHUFFLECLOUD && issue.labels.any? { |label| CloudTypes::CLOUDLABELS.include?(label.name) }
        total_words_added += 1
        if issue.labels.any? { |label| label.name == CloudTypes::CLOUDLABELS.last }
          current_words_added += 1
          current_contributors[issue.user.login] += 1
        end
      end
    end

    markdown = <<~HTML
    
<!--✏️WORDBOARD--> 
<h2 align="center">
Join the Global Boarding Pass ૮ ˶ᵔ ᵕ ᵔ˶ ა

### :thought_balloon: [Add your name](https://github.com/t1noo7/t1noo7/issues/new?template=addword.md&title=wordcloud%7Cadd%7C%3CINSERT-WORD%3E) to see your teleport in real time 𖦹.𖥔 ݁ ˖

:star2: Don't like the arrangement? [Regenerate it](https://github.com/t1noo7/t1noo7/issues/new?template=shufflecloud.md&title=wordcloud%7Cshuffle) :game_die:

<div align="center">

## Global Boarding Pass 🖍️🫠

![Words](https://img.shields.io/badge/Words%20in%20this%20Cloud-1-informational?labelColor=003995)
![Contributors](https://img.shields.io/badge/Cloud%20Contributors-1-blueviolet?labelColor=25004e)

<img src="wordcloud/wordcloud.png" alt="WordCloud" width="100%">
</div>

   HTML
    # TODO: [![Github Badge](https://img.shields.io/badge/-@username-24292e?style=flat&logo=Github&logoColor=white&link=https://github.com/username)](https://github.com/username)

    current_contributors.each do |username, count|
    end

    markdown.concat()

  end

  private

  def format_username(name)
    name.gsub('-', '--')
  end

  def previous_cloud_url
    url_end = CloudTypes::CLOUDPROMPTS[-2].gsub(' ', '-').gsub(':', '').gsub('?', '').downcase
    "previous_clouds/previous_clouds.md##{url_end}"
  end

  attr_reader :octokit
end

# frozen_string_literal: true

require "digest/md5"

module Jekyll
  module ThemeOverrides
    module HeadInjector
      module_function

      def inject!(document)
        output = document.output
        return unless output&.include?("</head>")
        return if output.include?("theme-overrides.css")

        site = document.site
        css_path = File.join(site.source, "assets", "css", "theme-overrides.css")
        return unless File.exist?(css_path)

        digest = Digest::MD5.file(css_path).hexdigest[0, 8]
        href = "#{site.baseurl}/assets/css/theme-overrides.css?v=#{digest}".gsub(%r{//+}, "/")
        link = %(  <link rel="stylesheet" href="#{href}">\n)
        document.output = output.sub("</head>", "#{link}</head>")
      end
    end
  end
end

Jekyll::Hooks.register %i[pages documents], :post_render do |document|
  Jekyll::ThemeOverrides::HeadInjector.inject!(document)
end

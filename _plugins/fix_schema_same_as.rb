# frozen_string_literal: true

# al_folio_core metadata.liquid pushes social[1].url for non-built-in keys.
# cv_pdf is a string path, so it becomes null in Schema.org sameAs. Drop it.
module Jekyll
  module FixSchemaSameAs
    module_function

    def sanitize!(document)
      output = document.output
      return unless output&.include?("application/ld+json") && output.include?('"sameAs"')

      fixed = output.gsub('"sameAs": [null,', '"sameAs": [')
                    .gsub('"sameAs": [null]', '"sameAs": []')
                    .gsub(", null", "")
                    .gsub(",null", "")
      document.output = fixed if fixed != output
    end
  end
end

Jekyll::Hooks.register %i[pages documents], :post_render do |document|
  Jekyll::FixSchemaSameAs.sanitize!(document)
end

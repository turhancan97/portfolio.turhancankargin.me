#!/usr/bin/env bash

_fixture_posts_repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
_fixture_posts_dir="${_fixture_posts_repo_root}/test/fixtures/posts"
_fixture_posts_installed=()

install_fixture_posts() {
  for src in "$@"; do
    cp "${_fixture_posts_dir}/${src}" "${_fixture_posts_repo_root}/_posts/${src}"
    _fixture_posts_installed+=("${src}")
  done
}

remove_fixture_posts() {
  for src in "${_fixture_posts_installed[@]}"; do
    rm -f "${_fixture_posts_repo_root}/_posts/${src}"
  done
}

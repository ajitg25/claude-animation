class ClaudeAnimation < Formula
  include Language::Python::Virtualenv

  desc "Brew-installable terminal animations — crack a whip and more"
  homepage "https://github.com/ajitg25/claude-animation"
  url "https://github.com/ajitg25/claude-animation/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "" # fill in after first release tag
  license "MIT"

  depends_on "python@3.12"

  resource "click" do
    url "https://files.pythonhosted.org/packages/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
  end

  def install
    virtualenv_install_with_resources
  end

  def post_install
    system "#{bin}/claude-animation", "install"
  end

  test do
    assert_match "whip", shell_output("#{bin}/claude-animation list")
  end
end

class Finance < Formula
  desc "Historical financial analysis and planning tool"
  homepage "https://github.com/itomek/finance"
  url "https://github.com/itomek/finance/releases/download/v0.1.0/finance-0.1.0.tar.gz"
  sha256 "placeholder_sha256_to_be_updated_after_release"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/finance", "--version"
  end
end
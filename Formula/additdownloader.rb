class Additdownloader < Formula
  desc "File registry and installer CLI"
  homepage "https://github.com/marzio-cloud/AdditDownloader"
  url "https://raw.githubusercontent.com/marzio-cloud/AdditDownloader/main/addit.py"
  version "1.0.0"
  sha256 "8eb98bb40d7c9ceca8df0a06368bd0bd658d32c1e1106abbb32dc6d936ec7bec"

  depends_on "python@3.13"

  def install
    libexec.install "addit.py"
    (bin/"additdownloader").write <<~EOS
      #!/bin/sh
      exec "#{Formula["python@3.13"].opt_bin}/python3" "#{libexec}/addit.py" "$@"
    EOS
    chmod 0755, bin/"additdownloader"
  end

  test do
    assert_match "AdditDownloader", shell_output("#{bin}/additdownloader help")
  end
end


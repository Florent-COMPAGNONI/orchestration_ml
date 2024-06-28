# instances/kestra_instance.tf
resource "google_compute_instance" "kestra_instance" {
  name         = "kestra-instance"
  machine_type = "n1-standard-1"
  zone         = "europe-west9-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y openjdk-11-jdk
    curl -L https://github.com/kestra-io/kestra/releases/download/0.17.3/kestra-0.17.3-bin.tar.gz | tar xz
    cd kestra-0.17.3
    ./bin/kestra start
  EOT
}

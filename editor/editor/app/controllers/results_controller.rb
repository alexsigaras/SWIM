class ResultsController < ApplicationController
  def index
  	@code = params[:token]
  	tmp_file = "#{Rails.root}/public/files/tmp.swim"
  	id = 0
  	while File.exists?(tmp_file) do
     tmp_file = "#{Rails.root}/public/files/tmp-#{id}.swim"        
     id += 1
   end
   File.open(tmp_file, 'wb') do |f|
     f.write  @code
   end
   @retval = `#{Rails.root}/public/bin/swim_osx #{tmp_file}`

 end


 respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @code }
      format.json { render json: @retval }
    end
  end
